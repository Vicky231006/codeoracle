"""
Python Parser Module for CodeOracle Ingestion Pipeline
Extracts structural information from Python source files using AST.
"""

import ast
import os
from typing import Dict, List, Any


def parse_python_file(filepath: str) -> Dict[str, Any]:
    """
    Parse a Python file and return structured data.
    
    Args:
        filepath: Path to the Python file
        
    Returns:
        Dictionary containing parsed file information
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST
        tree = ast.parse(content, filename=filepath)
        
        # Extract information
        imports = extract_imports(tree)
        functions = extract_functions(tree)
        classes = extract_classes(tree)
        exports = extract_exports(tree)
        complexity = calculate_file_complexity(tree)
        
        # Get file stats
        file_stats = os.stat(filepath)
        lines = content.count('\n') + 1
        
        return {
            'path': filepath,
            'language': 'python',
            'lines': lines,
            'size_bytes': file_stats.st_size,
            'imports': imports,
            'exports': exports,
            'functions': functions,
            'classes': classes,
            'complexity_score': complexity,
            'last_modified': None,  # Will be set by main script
            'is_test_file': False,  # Will be set by main script
            'is_config_file': False,  # Will be set by main script
            'raw_content': content[:8000]  # Truncate to 8000 chars
        }
    except Exception as e:
        # Return minimal data on parse error
        return {
            'path': filepath,
            'language': 'python',
            'lines': 0,
            'size_bytes': 0,
            'imports': [],
            'exports': [],
            'functions': [],
            'classes': [],
            'complexity_score': 0.0,
            'last_modified': None,
            'is_test_file': False,
            'is_config_file': False,
            'raw_content': '',
            'parse_error': str(e)
        }


def extract_imports(tree: ast.AST) -> List[str]:
    """
    Extract all import statements from the AST.
    
    Args:
        tree: AST tree of the Python file
        
    Returns:
        List of imported module names
    """
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
                # Also add specific imports
                for alias in node.names:
                    imports.append(f"{node.module}.{alias.name}")
    
    return list(set(imports))  # Remove duplicates


def extract_functions(tree: ast.AST) -> List[str]:
    """
    Extract all function names from the AST.
    
    Args:
        tree: AST tree of the Python file
        
    Returns:
        List of function names
    """
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions.append(node.name)
    
    return functions


def extract_classes(tree: ast.AST) -> List[str]:
    """
    Extract all class names from the AST.
    
    Args:
        tree: AST tree of the Python file
        
    Returns:
        List of class names
    """
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
    
    return classes


def extract_exports(tree: ast.AST) -> List[str]:
    """
    Extract module-level exports (functions and classes defined at top level).
    
    Args:
        tree: AST tree of the Python file
        
    Returns:
        List of exported names
    """
    exports = []
    
    # Only look at top-level definitions
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            if not node.name.startswith('_'):  # Exclude private functions
                exports.append(node.name)
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith('_'):  # Exclude private classes
                exports.append(node.name)
    
    return exports


def calculate_complexity(node: ast.AST) -> int:
    """
    Calculate cyclomatic complexity for a function node.
    
    Complexity is calculated by counting decision points:
    - if, elif
    - for, while
    - except
    - with
    - and, or (in boolean expressions)
    - lambda
    
    Args:
        node: AST node (typically a FunctionDef)
        
    Returns:
        Complexity score (integer)
    """
    complexity = 1  # Base complexity
    
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            # Count and/or operators
            complexity += len(child.values) - 1
        elif isinstance(child, ast.Lambda):
            complexity += 1
    
    return complexity


def calculate_file_complexity(tree: ast.AST) -> float:
    """
    Calculate overall file complexity score (0-100).
    
    Args:
        tree: AST tree of the Python file
        
    Returns:
        Normalized complexity score (0-100)
    """
    total_complexity = 0
    function_count = 0
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_count += 1
            total_complexity += calculate_complexity(node)
    
    if function_count == 0:
        return 0.0
    
    # Average complexity per function, normalized to 0-100 scale
    avg_complexity = total_complexity / function_count
    normalized = min(100.0, avg_complexity * 10)
    
    return round(normalized, 2)

# Made with Bob
