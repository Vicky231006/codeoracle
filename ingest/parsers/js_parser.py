"""
JavaScript/TypeScript Parser Module for CodeOracle Ingestion Pipeline
Extracts structural information from JavaScript/TypeScript source files using regex.
"""

import os
import re
from typing import Dict, List, Any


def parse_js_file(filepath: str) -> Dict[str, Any]:
    """
    Parse a JavaScript/TypeScript file and return structured data.
    
    Args:
        filepath: Path to the JS/TS file
        
    Returns:
        Dictionary containing parsed file information
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract information
        imports = extract_js_imports(content)
        functions = extract_js_functions(content)
        classes = extract_js_classes(content)
        exports = extract_js_exports(content)
        complexity = calculate_js_complexity(content)
        
        # Get file stats
        file_stats = os.stat(filepath)
        lines = content.count('\n') + 1
        
        # Determine language
        language = 'typescript' if filepath.endswith(('.ts', '.tsx')) else 'javascript'
        
        return {
            'path': filepath,
            'language': language,
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
        language = 'typescript' if filepath.endswith(('.ts', '.tsx')) else 'javascript'
        return {
            'path': filepath,
            'language': language,
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


def extract_js_imports(content: str) -> List[str]:
    """
    Extract require() and import statements from JavaScript/TypeScript.
    
    Args:
        content: File content as string
        
    Returns:
        List of imported module names
    """
    imports = []
    
    # ES6 import statements
    # import X from 'module'
    # import { X, Y } from 'module'
    # import * as X from 'module'
    import_pattern = r"import\s+(?:[\w\s{},*]+\s+from\s+)?['\"]([^'\"]+)['\"]"
    imports.extend(re.findall(import_pattern, content))
    
    # CommonJS require statements
    # const X = require('module')
    # require('module')
    require_pattern = r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
    imports.extend(re.findall(require_pattern, content))
    
    # Dynamic imports
    # import('module')
    dynamic_import_pattern = r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
    imports.extend(re.findall(dynamic_import_pattern, content))
    
    return list(set(imports))  # Remove duplicates


def extract_js_functions(content: str) -> List[str]:
    """
    Extract function names from JavaScript/TypeScript.
    
    Args:
        content: File content as string
        
    Returns:
        List of function names
    """
    functions = []
    
    # Function declarations
    # function name() {}
    func_decl_pattern = r"function\s+(\w+)\s*\("
    functions.extend(re.findall(func_decl_pattern, content))
    
    # Arrow functions assigned to variables
    # const name = () => {}
    # const name = async () => {}
    arrow_func_pattern = r"(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>"
    functions.extend(re.findall(arrow_func_pattern, content))
    
    # Method definitions in classes
    # methodName() {}
    # async methodName() {}
    method_pattern = r"(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{"
    # Filter out common keywords that might match
    potential_methods = re.findall(method_pattern, content)
    keywords = {'if', 'for', 'while', 'switch', 'catch', 'function', 'class'}
    functions.extend([m for m in potential_methods if m not in keywords])
    
    return list(set(functions))  # Remove duplicates


def extract_js_classes(content: str) -> List[str]:
    """
    Extract class names from JavaScript/TypeScript.
    
    Args:
        content: File content as string
        
    Returns:
        List of class names
    """
    classes = []
    
    # Class declarations
    # class ClassName {}
    # export class ClassName {}
    # export default class ClassName {}
    class_pattern = r"(?:export\s+(?:default\s+)?)?class\s+(\w+)"
    classes.extend(re.findall(class_pattern, content))
    
    return list(set(classes))  # Remove duplicates


def extract_js_exports(content: str) -> List[str]:
    """
    Extract exported names from JavaScript/TypeScript.
    
    Args:
        content: File content as string
        
    Returns:
        List of exported names
    """
    exports = []
    
    # Named exports
    # export { name1, name2 }
    named_export_pattern = r"export\s*\{\s*([^}]+)\s*\}"
    matches = re.findall(named_export_pattern, content)
    for match in matches:
        # Split by comma and clean up
        names = [n.strip().split()[0] for n in match.split(',')]
        exports.extend(names)
    
    # Export declarations
    # export function name() {}
    # export class Name {}
    # export const name = ...
    export_decl_pattern = r"export\s+(?:async\s+)?(?:function|class|const|let|var)\s+(\w+)"
    exports.extend(re.findall(export_decl_pattern, content))
    
    # Default exports with names
    # export default ClassName
    # export default function name() {}
    default_export_pattern = r"export\s+default\s+(?:function\s+)?(\w+)"
    exports.extend(re.findall(default_export_pattern, content))
    
    # module.exports
    # module.exports = { name1, name2 }
    # module.exports.name = ...
    module_exports_pattern = r"module\.exports\.(\w+)"
    exports.extend(re.findall(module_exports_pattern, content))
    
    # module.exports = { ... }
    module_exports_obj_pattern = r"module\.exports\s*=\s*\{\s*([^}]+)\s*\}"
    matches = re.findall(module_exports_obj_pattern, content)
    for match in matches:
        names = [n.strip().split(':')[0].strip() for n in match.split(',')]
        exports.extend(names)
    
    return list(set(exports))  # Remove duplicates


def calculate_js_complexity(content: str) -> float:
    """
    Calculate complexity score for JavaScript/TypeScript file (0-100).
    
    Counts decision points:
    - if, else if
    - for, while, do-while
    - switch cases
    - catch blocks
    - ternary operators
    - && and || in conditions
    
    Args:
        content: File content as string
        
    Returns:
        Normalized complexity score (0-100)
    """
    complexity = 1  # Base complexity
    
    # Count if statements
    complexity += len(re.findall(r'\bif\s*\(', content))
    
    # Count else if
    complexity += len(re.findall(r'\belse\s+if\s*\(', content))
    
    # Count loops
    complexity += len(re.findall(r'\bfor\s*\(', content))
    complexity += len(re.findall(r'\bwhile\s*\(', content))
    complexity += len(re.findall(r'\bdo\s*\{', content))
    
    # Count switch cases
    complexity += len(re.findall(r'\bcase\s+', content))
    
    # Count catch blocks
    complexity += len(re.findall(r'\bcatch\s*\(', content))
    
    # Count ternary operators
    complexity += len(re.findall(r'\?[^:]+:', content))
    
    # Count logical operators in conditions (simplified)
    complexity += len(re.findall(r'&&', content))
    complexity += len(re.findall(r'\|\|', content))
    
    # Estimate number of functions for normalization
    function_count = max(1, len(extract_js_functions(content)))
    
    # Average complexity per function, normalized to 0-100 scale
    avg_complexity = complexity / function_count
    normalized = min(100.0, avg_complexity * 10)
    
    return round(normalized, 2)

# Made with Bob
