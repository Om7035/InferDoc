"""
Local Testing Script for InferDoc

This script allows you to test InferDoc on a single Python file locally.
It runs the complete pipeline: parse → enhance → analyze → generate.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from inferdoc.parser import parse_python_file, get_module_summary
from inferdoc.generator import generate_markdown, save_markdown
from inferdoc.ai_enhancer import enhance_structure_with_ai, test_api_connection
from inferdoc.git_analyzer import get_file_summary, is_git_repository


# Configuration
TEST_FILE_PATH = 'inferdoc/parser.py'  # Default test file
REPO_PATH = '.'
TEMPLATE_DIR = 'templates'
TEMPLATE_NAME = 'module.md.j2'
OUTPUT_DIR = 'docs'


def main(file_path: str = None, skip_ai: bool = False, skip_git: bool = False):
    """
    Run CodeScribe on a single file.
    
    Args:
        file_path: Path to the Python file to document (default: TEST_FILE_PATH)
        skip_ai: Skip AI enhancement (useful for testing without API key)
        skip_git: Skip git analysis
    """
    # Use default if no file specified
    if not file_path:
        file_path = TEST_FILE_PATH
    
    print("=" * 70)
    print("🚀 InferDoc - AI-Powered Documentation Generator")
    print("=" * 70)
    print(f"\n📄 Processing file: {file_path}\n")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return 1
    
    try:
        # Step 1: Parse the file
        print("📖 Step 1: Parsing file structure...")
        structure = parse_python_file(file_path)
        print(f"   ✓ {get_module_summary(structure)}")
        
        # Step 2: Enhance with AI docstrings
        if not skip_ai:
            print("\n🤖 Step 2: Enhancing with AI-generated docstrings...")
            print("   Testing API connection...")
            if test_api_connection():
                enhanced_structure = enhance_structure_with_ai(structure, verbose=True)
            else:
                print("   ⚠️  Skipping AI enhancement (API not available)")
                enhanced_structure = structure
        else:
            print("\n⏭️  Step 2: Skipping AI enhancement (--skip-ai flag)")
            enhanced_structure = structure
        
        # Step 3: Get Git history
        if not skip_git:
            print("\n📊 Step 3: Analyzing Git history...")
            if is_git_repository(REPO_PATH):
                summary = get_file_summary(REPO_PATH, file_path, limit=5)
                print(f"   ✓ Generated summary from recent commits")
            else:
                print("   ⚠️  Not a git repository, skipping git analysis")
                summary = None
        else:
            print("\n⏭️  Step 3: Skipping git analysis (--skip-git flag)")
            summary = None
        
        # Step 4: Generate Markdown
        print("\n📝 Step 4: Generating Markdown documentation...")
        module_name = os.path.basename(file_path)
        md_content = generate_markdown(
            enhanced_structure,
            TEMPLATE_DIR,
            TEMPLATE_NAME,
            module_name,
            summary
        )
        print(f"   ✓ Generated {len(md_content)} characters of documentation")
        
        # Step 5: Write to docs folder
        print("\n💾 Step 5: Saving documentation...")
        output_filename = module_name.replace('.py', '.md')
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        save_markdown(md_content, output_path)
        print(f"   ✓ Saved to: {output_path}")
        
        # Success!
        print("\n" + "=" * 70)
        print("✅ Documentation generated successfully!")
        print("=" * 70)
        print("\n📚 Next steps:")
        print("   1. Review the generated documentation:")
        print(f"      {output_path}")
        print("\n   2. Preview with MkDocs:")
        print("      mkdocs serve")
        print("\n   3. Visit: http://127.0.0.1:8000")
        print("\n" + "=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate documentation for a Python file using InferDoc"
    )
    parser.add_argument(
        'file',
        nargs='?',
        default=TEST_FILE_PATH,
        help=f'Python file to document (default: {TEST_FILE_PATH})'
    )
    parser.add_argument(
        '--skip-ai',
        action='store_true',
        help='Skip AI enhancement (useful for testing without API key)'
    )
    parser.add_argument(
        '--skip-git',
        action='store_true',
        help='Skip git history analysis'
    )
    
    args = parser.parse_args()
    
    exit_code = main(args.file, skip_ai=args.skip_ai, skip_git=args.skip_git)
    sys.exit(exit_code)
