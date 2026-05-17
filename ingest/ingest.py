"""
CodeOracle Repository Ingestion Pipeline
Main script for processing repositories into structured JSON manifests.
"""

import argparse
import json
import logging
import os
import re
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

# Import parsers
from ingest.parsers.python_parser import parse_python_file
from ingest.parsers.js_parser import parse_js_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# File extensions to process
PYTHON_EXTENSIONS = {'.py'}
JAVASCRIPT_EXTENSIONS = {'.js', '.jsx', '.ts', '.tsx'}
SUPPORTED_EXTENSIONS = PYTHON_EXTENSIONS | JAVASCRIPT_EXTENSIONS

# Directories to skip
SKIP_DIRECTORIES = {
    'node_modules', 'venv', '__pycache__', '.git', 
    'dist', 'build', '.venv', 'env', '.env',
    'coverage', '.pytest_cache', '.mypy_cache'
}


def is_test_file(filepath: str) -> bool:
    """
    Detect if file is a test file.
    
    Patterns:
    - test_*.py, *_test.py
    - *.test.js, *.spec.js, *.test.ts, *.spec.ts
    - /tests/, /test/, /__tests__/
    
    Args:
        filepath: Path to the file
        
    Returns:
        True if file is a test file
    """
    filepath_lower = filepath.lower()
    filename = os.path.basename(filepath_lower)
    
    # Check filename patterns
    if filename.startswith('test_') or filename.endswith('_test.py'):
        return True
    if '.test.' in filename or '.spec.' in filename:
        return True
    
    # Check directory patterns
    path_parts = filepath_lower.split(os.sep)
    if any(part in {'test', 'tests', '__tests__', 'spec', 'specs'} for part in path_parts):
        return True
    
    return False


def is_config_file(filepath: str) -> bool:
    """
    Detect if file is a config file.
    
    Patterns:
    - config.*, setup.py, package.json, requirements.txt
    - .env, *.config.js, *.config.ts
    - tsconfig.json, webpack.config.js, babel.config.js, etc.
    
    Args:
        filepath: Path to the file
        
    Returns:
        True if file is a config file
    """
    filename = os.path.basename(filepath).lower()
    
    # Common config file patterns
    config_patterns = [
        r'^config\.',
        r'\.config\.(js|ts|json)$',
        r'^setup\.py$',
        r'^package\.json$',
        r'^requirements.*\.txt$',
        r'^pipfile$',
        r'^\.env',
        r'config\.json$',
        r'^tsconfig\.json$',
        r'^webpack\.config',
        r'^babel\.config',
        r'^jest\.config',
        r'^rollup\.config',
        r'^vite\.config'
    ]
    
    for pattern in config_patterns:
        if re.search(pattern, filename):
            return True
    
    return False


def detect_entry_points(files_data: List[Dict[str, Any]]) -> List[str]:
    """
    Identify likely entry point files.
    
    Patterns:
    - main.py, __main__.py, app.py, server.py
    - index.js, app.js, server.js, main.js
    - Files with if __name__ == "__main__" in Python
    
    Args:
        files_data: List of parsed file data
        
    Returns:
        List of entry point file paths
    """
    entry_points = []
    
    for file_data in files_data:
        filepath = file_data['path']
        filename = os.path.basename(filepath).lower()
        
        # Check common entry point filenames
        entry_filenames = {
            'main.py', '__main__.py', 'app.py', 'server.py',
            'index.js', 'app.js', 'server.js', 'main.js',
            'index.ts', 'app.ts', 'server.ts', 'main.ts'
        }
        
        if filename in entry_filenames:
            entry_points.append(filepath)
            continue
        
        # Check for Python __main__ pattern
        if file_data['language'] == 'python':
            raw_content = file_data.get('raw_content', '')
            if '__name__' in raw_content and '__main__' in raw_content:
                entry_points.append(filepath)
    
    return entry_points


def extract_external_dependencies(repo_path: str, language: str) -> List[Dict[str, str]]:
    """
    Extract external package dependencies.
    
    Python: Parse requirements.txt, setup.py, Pipfile
    JavaScript: Parse package.json
    
    Args:
        repo_path: Path to the repository
        language: Primary language of the repository
        
    Returns:
        List of dependencies with name and version
    """
    dependencies = []
    
    if language == 'python':
        # Check requirements.txt
        req_files = ['requirements.txt', 'requirements-dev.txt', 'requirements-test.txt']
        for req_file in req_files:
            req_path = os.path.join(repo_path, req_file)
            if os.path.exists(req_path):
                try:
                    with open(req_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Parse package==version or package>=version
                                match = re.match(r'^([a-zA-Z0-9_-]+)([>=<~!]+)(.+)$', line)
                                if match:
                                    dependencies.append({
                                        'name': match.group(1),
                                        'version': match.group(3)
                                    })
                                else:
                                    # Package without version
                                    pkg_name = line.split('[')[0].strip()
                                    if pkg_name:
                                        dependencies.append({
                                            'name': pkg_name,
                                            'version': 'unknown'
                                        })
                except Exception as e:
                    logger.warning(f"Error parsing {req_file}: {e}")
        
        # Check Pipfile
        pipfile_path = os.path.join(repo_path, 'Pipfile')
        if os.path.exists(pipfile_path):
            try:
                with open(pipfile_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple regex to extract package names
                    packages = re.findall(r'^([a-zA-Z0-9_-]+)\s*=', content, re.MULTILINE)
                    for pkg in packages:
                        if pkg not in ['python', 'packages', 'dev-packages']:
                            dependencies.append({
                                'name': pkg,
                                'version': 'unknown'
                            })
            except Exception as e:
                logger.warning(f"Error parsing Pipfile: {e}")
    
    elif language in ['javascript', 'typescript']:
        # Check package.json
        package_json_path = os.path.join(repo_path, 'package.json')
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    
                    # Get dependencies
                    for dep_type in ['dependencies', 'devDependencies']:
                        if dep_type in package_data:
                            for name, version in package_data[dep_type].items():
                                dependencies.append({
                                    'name': name,
                                    'version': version
                                })
            except Exception as e:
                logger.warning(f"Error parsing package.json: {e}")
    
    return dependencies


def build_dependency_graph(files_data: List[Dict[str, Any]], repo_path: str) -> Dict[str, Any]:
    """
    Build a graph of file dependencies.
    
    Args:
        files_data: List of parsed file data
        repo_path: Path to the repository root
        
    Returns:
        Dictionary with nodes and edges
    """
    nodes = []
    edges = []
    
    # Create a mapping of module names to file paths
    file_map = {}
    for file_data in files_data:
        filepath = file_data['path']
        
        # Add node
        nodes.append({
            'id': filepath,
            'label': os.path.basename(filepath)
        })
        
        # Map module name to file path (handle both / and \ separators)
        normalized_path = filepath.replace('\\', '/')
        module_name = os.path.splitext(normalized_path)[0].replace('/', '.')
        file_map[module_name] = filepath
        
        # Also map just the filename without extension
        filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
        if filename_no_ext not in file_map:
            file_map[filename_no_ext] = filepath
    
    # Create edges based on imports
    for file_data in files_data:
        source_path = file_data['path']
        
        for import_name in file_data.get('imports', []):
            target_path = None
            
            # Extract base module name (before any dots for sub-imports)
            base_import = import_name.split('.')[0]
            
            # Check if this is an internal module
            if base_import in file_map:
                target_path = file_map[base_import]
            
            # Add edge if target found and different from source
            if target_path and target_path != source_path:
                edge_type = 'import' if file_data['language'] == 'python' else 'require'
                edges.append({
                    'source': source_path,
                    'target': target_path,
                    'type': edge_type
                })
    
    return {
        'nodes': nodes,
        'edges': edges
    }


def process_repository(repo_path: str, language: Optional[str] = None) -> Dict[str, Any]:
    """
    Process a repository and extract all information.
    
    Args:
        repo_path: Path to the repository
        language: Primary language (auto-detect if None)
        
    Returns:
        Complete repository manifest
    """
    logger.info(f"Processing repository: {repo_path}")
    
    files_data = []
    total_lines = 0
    file_count = 0
    language_counts = {'python': 0, 'javascript': 0, 'typescript': 0}
    
    # Walk through repository
    for root, dirs, files in os.walk(repo_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()
            
            # Only process supported files
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            
            file_count += 1
            
            # Log progress every 10 files
            if file_count % 10 == 0:
                logger.info(f"Processed {file_count} files...")
            
            # Parse file based on extension
            try:
                if ext in PYTHON_EXTENSIONS:
                    file_data = parse_python_file(filepath)
                    language_counts['python'] += 1
                elif ext in JAVASCRIPT_EXTENSIONS:
                    file_data = parse_js_file(filepath)
                    if file_data['language'] == 'typescript':
                        language_counts['typescript'] += 1
                    else:
                        language_counts['javascript'] += 1
                else:
                    continue
                
                # Set additional flags
                file_data['is_test_file'] = is_test_file(filepath)
                file_data['is_config_file'] = is_config_file(filepath)
                
                # Convert to relative path
                file_data['path'] = os.path.relpath(filepath, repo_path)
                
                # Add to collection
                files_data.append(file_data)
                total_lines += file_data['lines']
                
            except Exception as e:
                logger.warning(f"Error processing {filepath}: {e}")
                continue
    
    logger.info(f"Completed processing {file_count} files")
    
    # Determine primary language
    if language is None:
        language = max(language_counts.items(), key=lambda x: x[1])[0]
        if language_counts[language] == 0:
            language = 'unknown'
    
    # Build dependency graph
    logger.info("Building dependency graph...")
    dependency_graph = build_dependency_graph(files_data, repo_path)
    
    # Detect entry points
    logger.info("Detecting entry points...")
    entry_points = detect_entry_points(files_data)
    
    # Extract external dependencies
    logger.info("Extracting external dependencies...")
    external_deps = extract_external_dependencies(repo_path, language)
    
    # Build manifest
    repo_name = os.path.basename(os.path.abspath(repo_path))
    manifest = {
        'repo_name': repo_name,
        'language_primary': language,
        'total_files': len(files_data),
        'total_lines': total_lines,
        'ingested_at': datetime.now().astimezone().replace(microsecond=0).isoformat(),
        'files': files_data,
        'dependency_graph': dependency_graph,
        'entry_points': entry_points,
        'external_dependencies': external_deps
    }
    
    return manifest


def clone_git_repo(url: str, temp_dir: str) -> str:
    """
    Clone a git repository to a temporary directory.
    
    Args:
        url: Git repository URL
        temp_dir: Temporary directory path
        
    Returns:
        Path to cloned repository
    """
    try:
        import git
        logger.info(f"Cloning repository from {url}...")
        repo = git.Repo.clone_from(url, temp_dir)
        logger.info("Clone completed")
        return temp_dir
    except ImportError:
        logger.error("GitPython not installed. Install with: pip install gitpython")
        raise
    except Exception as e:
        logger.error(f"Error cloning repository: {e}")
        raise


def extract_zip(zip_path: str, temp_dir: str) -> str:
    """
    Extract a ZIP file to a temporary directory.
    
    Args:
        zip_path: Path to ZIP file
        temp_dir: Temporary directory path
        
    Returns:
        Path to extracted contents
    """
    logger.info(f"Extracting ZIP file: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Find the root directory (in case ZIP has a single root folder)
    contents = os.listdir(temp_dir)
    if len(contents) == 1 and os.path.isdir(os.path.join(temp_dir, contents[0])):
        return os.path.join(temp_dir, contents[0])
    
    return temp_dir


def main():
    """Main entry point for the ingestion script."""
    parser = argparse.ArgumentParser(
        description='CodeOracle Repository Ingestion Pipeline'
    )
    parser.add_argument(
        '--source',
        required=True,
        help='Source: local path, GitHub URL, or ZIP file'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output path for repo_manifest.json'
    )
    parser.add_argument(
        '--language',
        choices=['python', 'javascript', 'typescript'],
        help='Primary language (auto-detect if not specified)'
    )
    
    args = parser.parse_args()
    
    temp_dir = None
    try:
        # Determine source type and get repository path
        source = args.source
        
        if source.startswith('http://') or source.startswith('https://'):
            # Git URL
            temp_dir = tempfile.mkdtemp(prefix='codeoracle_')
            repo_path = clone_git_repo(source, temp_dir)
        elif source.endswith('.zip'):
            # ZIP file
            temp_dir = tempfile.mkdtemp(prefix='codeoracle_')
            repo_path = extract_zip(source, temp_dir)
        else:
            # Local path
            repo_path = os.path.abspath(source)
            if not os.path.exists(repo_path):
                logger.error(f"Path does not exist: {repo_path}")
                return 1
        
        # Process repository
        manifest = process_repository(repo_path, args.language)
        
        # Write output
        output_path = args.output
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"Manifest written to: {output_path}")
        logger.info(f"Total files: {manifest['total_files']}")
        logger.info(f"Total lines: {manifest['total_lines']}")
        logger.info(f"Primary language: {manifest['language_primary']}")
        logger.info(f"Entry points: {len(manifest['entry_points'])}")
        logger.info(f"External dependencies: {len(manifest['external_dependencies'])}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during ingestion: {e}", exc_info=True)
        return 1
    
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            logger.info("Cleaned up temporary files")


if __name__ == '__main__':
    exit(main())

# Made with Bob
