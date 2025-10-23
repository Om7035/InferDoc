"""
Python Code Parser Module

This module provides functionality to parse Python source files and extract
their structure including classes, functions, methods, and docstrings using
Python's Abstract Syntax Tree (AST).
"""

import ast
from typing import Dict, List, Any, Optional


def get_source_segment(source_lines: List[str], node: ast.AST) -> str:
    """
    Extract the full source code of an AST node.
    
    Args:
        source_lines: List of source code lines with line endings preserved
        node: AST node to extract source from
        
    Returns:
        str: The source code of the node as a string
    """
    if not hasattr(node, 'lineno') or not hasattr(node, 'end_lineno'):
        return ""
    
    lines = source_lines[node.lineno - 1:node.end_lineno]
    return "".join(lines)


def extract_function_info(node: ast.FunctionDef, source_lines: List[str]) -> Dict[str, Any]:
    """
    Extract information from a function or method definition.
    
    Args:
        node: AST FunctionDef node
        source_lines: Source code lines for extracting code segment
        
    Returns:
        dict: Function information including name, args, docstring, and code
    """
    return {
        'name': node.name,
        'args': [arg.arg for arg in node.args.args],
        'docstring': ast.get_docstring(node),
        'code': get_source_segment(source_lines, node),
        'lineno': node.lineno,
        'decorators': [ast.unparse(dec) for dec in node.decorator_list] if node.decorator_list else []
    }


def extract_class_info(node: ast.ClassDef, source_lines: List[str]) -> Dict[str, Any]:
    """
    Extract information from a class definition.
    
    Args:
        node: AST ClassDef node
        source_lines: Source code lines for extracting code segment
        
    Returns:
        dict: Class information including name, docstring, code, and methods
    """
    class_info = {
        'name': node.name,
        'docstring': ast.get_docstring(node),
        'code': get_source_segment(source_lines, node),
        'lineno': node.lineno,
        'methods': [],
        'bases': [ast.unparse(base) for base in node.bases] if node.bases else [],
        'decorators': [ast.unparse(dec) for dec in node.decorator_list] if node.decorator_list else []
    }
    
    # Extract methods from the class
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            method_info = extract_function_info(item, source_lines)
            class_info['methods'].append(method_info)
    
    return class_info


def parse_python_file(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse a Python file and extract its structure.
    
    This function analyzes a Python source file and extracts information about
    all classes and functions defined in it, including their docstrings,
    arguments, and source code.
    
    Args:
        file_path: Path to the Python file to parse
        
    Returns:
        dict: A dictionary containing two keys:
            - 'classes': List of class information dictionaries
            - 'functions': List of function information dictionaries
            
    Raises:
        FileNotFoundError: If the specified file does not exist
        SyntaxError: If the file contains invalid Python syntax
        
    Example:
        >>> structure = parse_python_file('my_module.py')
        >>> print(f"Found {len(structure['classes'])} classes")
        >>> print(f"Found {len(structure['functions'])} functions")
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {str(e)}")
    
    # Split source into lines while preserving line endings
    source_lines = source_code.splitlines(keepends=True)
    
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in {file_path}: {str(e)}")
    
    structure = {
        'classes': [],
        'functions': [],
        'module_docstring': ast.get_docstring(tree)
    }
    
    # Walk through top-level nodes only to avoid duplicates
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_info = extract_class_info(node, source_lines)
            structure['classes'].append(class_info)
            
        elif isinstance(node, ast.FunctionDef):
            function_info = extract_function_info(node, source_lines)
            structure['functions'].append(function_info)
    
    return structure


def get_module_summary(structure: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Generate a brief summary of the module structure.
    
    Args:
        structure: Parsed structure dictionary from parse_python_file
        
    Returns:
        str: A human-readable summary of the module
    """
    num_classes = len(structure['classes'])
    num_functions = len(structure['functions'])
    num_methods = sum(len(cls['methods']) for cls in structure['classes'])
    
    summary_parts = []
    
    if num_classes > 0:
        summary_parts.append(f"{num_classes} class{'es' if num_classes != 1 else ''}")
    if num_functions > 0:
        summary_parts.append(f"{num_functions} function{'s' if num_functions != 1 else ''}")
    if num_methods > 0:
        summary_parts.append(f"{num_methods} method{'s' if num_methods != 1 else ''}")
    
    if not summary_parts:
        return "Empty module"
    
    return f"Module contains: {', '.join(summary_parts)}"


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            result = parse_python_file(file_path)
            print(f"\n{get_module_summary(result)}")
            print(f"\nModule docstring: {result.get('module_docstring', 'None')}")
            
            if result['classes']:
                print("\nClasses:")
                for cls in result['classes']:
                    print(f"  - {cls['name']} ({len(cls['methods'])} methods)")
            
            if result['functions']:
                print("\nFunctions:")
                for func in result['functions']:
                    print(f"  - {func['name']}({', '.join(func['args'])})")
                    
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python parser.py <python_file>")
        sys.exit(1)
