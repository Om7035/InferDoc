"""
Main Production Script for InferDoc

This script processes all Python files in a project and generates
comprehensive documentation for each one.
"""

import os
import sys
import glob
from pathlib import Path
from typing import List, Dict

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from inferdoc.parser import parse_python_file, get_module_summary
from inferdoc.generator import generate_markdown, save_markdown, generate_index_page
from inferdoc.ai_enhancer import enhance_structure_with_ai, test_api_connection
from inferdoc.git_analyzer import get_file_summary, is_git_repository


def find_python_files(
    directory: str,
    exclude_patterns: List[str] = None
) -> List[str]:
    """
    Find all Python files in a directory recursively.
    
    Args:
        directory: Root directory to search
        exclude_patterns: List of patterns to exclude (e.g., ['venv', '__pycache__'])
        
    Returns:
        list: List of Python file paths
    """
    if exclude_patterns is None:
        exclude_patterns = [
            'venv', 'env', '.venv',
            '__pycache__', '.git',
            'site-packages', 'dist', 'build',
            '.eggs', '*.egg-info'
        ]
    
    python_files = []
    
    for root, dirs, files in os.walk(directory):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
        
        # Find Python files
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                # Skip if matches exclude pattern
                if not any(pattern in file_path for pattern in exclude_patterns):
                    python_files.append(file_path)
    
    return sorted(python_files)


def process_file(
    file_path: str,
    repo_path: str,
    template_dir: str,
    template_name: str,
    output_dir: str,
    skip_ai: bool = False,
    skip_git: bool = False,
    verbose: bool = True
) -> Dict[str, str]:
    """
    Process a single Python file through the complete pipeline.
    
    Args:
        file_path: Path to the Python file
        repo_path: Path to the git repository root
        template_dir: Directory containing templates
        template_name: Name of the template file
        output_dir: Directory to save output
        skip_ai: Skip AI enhancement
        skip_git: Skip git analysis
        verbose: Print progress messages
        
    Returns:
        dict: Information about the processed file (name, path, status)
    """
    if verbose:
        print(f"\n📄 Processing: {file_path}")
    
    try:
        # Parse
        structure = parse_python_file(file_path)
        if verbose:
            print(f"   ✓ Parsed: {get_module_summary(structure)}")
        
        # Enhance with AI
        if not skip_ai:
            enhanced_structure = enhance_structure_with_ai(structure, verbose=False)
            if verbose:
                print(f"   ✓ AI enhancement complete")
        else:
            enhanced_structure = structure
        
        # Get git summary
        summary = None
        if not skip_git and is_git_repository(repo_path):
            summary = get_file_summary(repo_path, file_path, limit=5)
            if verbose and summary:
                print(f"   ✓ Git analysis complete")
        
        # Generate markdown
        module_name = os.path.basename(file_path)
        md_content = generate_markdown(
            enhanced_structure,
            template_dir,
            template_name,
            module_name,
            summary
        )
        
        # Save
        # Create relative path structure in output
        rel_path = os.path.relpath(file_path, repo_path)
        output_filename = rel_path.replace('.py', '.md').replace(os.sep, '_')
        output_path = os.path.join(output_dir, output_filename)
        
        save_markdown(md_content, output_path)
        if verbose:
            print(f"   ✓ Saved to: {output_path}")
        
        return {
            'name': module_name,
            'path': output_filename,
            'status': 'success',
            'source': file_path
        }
        
    except Exception as e:
        if verbose:
            print(f"   ❌ Error: {e}")
        return {
            'name': os.path.basename(file_path),
            'path': None,
            'status': 'error',
            'error': str(e),
            'source': file_path
        }


def main(
    source_dir: str = 'inferdoc',
    output_dir: str = 'docs',
    template_dir: str = 'templates',
    template_name: str = 'module.md.j2',
    skip_ai: bool = False,
    skip_git: bool = False,
    project_name: str = "InferDoc Documentation"
):
    """
    Main function to process all Python files in a project.
    
    Args:
        source_dir: Directory containing Python files to document
        output_dir: Directory to save generated documentation
        template_dir: Directory containing Jinja2 templates
        template_name: Name of the template file
        skip_ai: Skip AI enhancement
        skip_git: Skip git analysis
        project_name: Name of the project for index page
    """
    print("=" * 70)
    print("🚀 InferDoc - Batch Documentation Generator")
    print("=" * 70)
    
    # Find all Python files
    print(f"\n🔍 Searching for Python files in: {source_dir}")
    python_files = find_python_files(source_dir)
    print(f"   Found {len(python_files)} Python files")
    
    if not python_files:
        print("   ⚠️  No Python files found!")
        return 1
    
    # Test API if not skipping AI
    if not skip_ai:
        print("\n🤖 Testing OpenAI API connection...")
        if not test_api_connection():
            print("   ⚠️  Continuing without AI enhancement")
            skip_ai = True
    
    # Process each file
    print(f"\n📚 Processing {len(python_files)} files...")
    print("=" * 70)
    
    results = []
    for file_path in python_files:
        result = process_file(
            file_path,
            repo_path='.',
            template_dir=template_dir,
            template_name=template_name,
            output_dir=output_dir,
            skip_ai=skip_ai,
            skip_git=skip_git,
            verbose=True
        )
        results.append(result)
    
    # Generate index page
    print("\n📑 Generating index page...")
    successful_modules = [r for r in results if r['status'] == 'success']
    index_content = generate_index_page(successful_modules, template_dir, project_name)
    index_path = os.path.join(output_dir, 'api_index.md')
    save_markdown(index_content, index_path)
    print(f"   ✓ Saved index to: {index_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Summary")
    print("=" * 70)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = sum(1 for r in results if r['status'] == 'error')
    
    print(f"\n✅ Successfully processed: {success_count}/{len(results)} files")
    if error_count > 0:
        print(f"❌ Errors: {error_count}")
        print("\nFailed files:")
        for result in results:
            if result['status'] == 'error':
                print(f"   - {result['source']}: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 70)
    print("📚 Next steps:")
    print("   1. Review generated documentation in:", output_dir)
    print("   2. Preview with MkDocs: mkdocs serve")
    print("   3. Visit: http://127.0.0.1:8000")
    print("   4. Build static site: mkdocs build")
    print("=" * 70 + "\n")
    
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate documentation for all Python files in a project"
    )
    parser.add_argument(
        '--source-dir',
        default='inferdoc',
        help='Directory containing Python files (default: inferdoc)'
    )
    parser.add_argument(
        '--output-dir',
        default='docs',
        help='Output directory for documentation (default: docs)'
    )
    parser.add_argument(
        '--template-dir',
        default='templates',
        help='Directory containing templates (default: templates)'
    )
    parser.add_argument(
        '--template-name',
        default='module.md.j2',
        help='Template file name (default: module.md.j2)'
    )
    parser.add_argument(
        '--skip-ai',
        action='store_true',
        help='Skip AI enhancement'
    )
    parser.add_argument(
        '--skip-git',
        action='store_true',
        help='Skip git analysis'
    )
    parser.add_argument(
        '--project-name',
        default='InferDoc Documentation',
        help='Project name for index page'
    )
    
    args = parser.parse_args()
    
    exit_code = main(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        template_dir=args.template_dir,
        template_name=args.template_name,
        skip_ai=args.skip_ai,
        skip_git=args.skip_git,
        project_name=args.project_name
    )
    
    sys.exit(exit_code)
