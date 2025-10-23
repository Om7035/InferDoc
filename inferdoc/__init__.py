"""
InferDoc - AI-Powered Documentation Generator

An automated documentation system that generates and maintains
comprehensive documentation for Python projects using AI.
"""

__version__ = "1.0.0"
__author__ = "InferDoc Team"
__license__ = "MIT"

from .parser import parse_python_file
from .generator import generate_markdown
from .ai_enhancer import enhance_structure_with_ai
from .git_analyzer import get_commit_history, summarize_commits_with_ai

__all__ = [
    "parse_python_file",
    "generate_markdown",
    "enhance_structure_with_ai",
    "get_commit_history",
    "summarize_commits_with_ai",
]
