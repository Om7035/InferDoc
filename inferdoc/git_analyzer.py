"""
Git Analysis Module

This module provides functionality to analyze git commit history
and generate summaries using AI.
"""

import os
from typing import List, Optional
from datetime import datetime

try:
    import git
    from git import Repo, InvalidGitRepositoryError, GitCommandError
except ImportError:
    raise ImportError(
        "GitPython library not installed. Install it with: pip install GitPython"
    )

from .ai_enhancer import client, DEFAULT_MODEL


def is_git_repository(repo_path: str) -> bool:
    """
    Check if a directory is a git repository.
    
    Args:
        repo_path: Path to check
        
    Returns:
        bool: True if it's a git repository, False otherwise
    """
    try:
        _ = Repo(repo_path)
        return True
    except (InvalidGitRepositoryError, git.exc.NoSuchPathError):
        return False


def get_commit_history(
    repo_path: str,
    file_path: str,
    limit: int = 5
) -> List[dict]:
    """
    Get the last 'limit' commits for a specific file.
    
    Args:
        repo_path: Path to the git repository root
        file_path: Path to the file (relative to repo root or absolute)
        limit: Maximum number of commits to retrieve
        
    Returns:
        list: List of commit dictionaries with 'message', 'author', 'date', and 'hash'
        
    Example:
        >>> commits = get_commit_history('.', 'my_module.py', limit=5)
        >>> for commit in commits:
        ...     print(f"{commit['date']}: {commit['message']}")
    """
    try:
        repo = Repo(repo_path)
        
        # Convert absolute path to relative if needed
        if os.path.isabs(file_path):
            file_path = os.path.relpath(file_path, repo_path)
        
        # Get commits for the specific file
        commits = list(repo.iter_commits(paths=file_path, max_count=limit))
        
        commit_data = []
        for commit in commits:
            commit_data.append({
                'message': commit.message.strip(),
                'author': commit.author.name,
                'date': datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M'),
                'hash': commit.hexsha[:7]  # Short hash
            })
        
        return commit_data
        
    except InvalidGitRepositoryError:
        print(f"Warning: {repo_path} is not a git repository")
        return []
    except GitCommandError as e:
        print(f"Warning: Git command error: {e}")
        return []
    except Exception as e:
        print(f"Warning: Error getting git history: {e}")
        return []


def get_commit_messages(
    repo_path: str,
    file_path: str,
    limit: int = 5
) -> List[str]:
    """
    Get just the commit messages for a specific file.
    
    Args:
        repo_path: Path to the git repository root
        file_path: Path to the file
        limit: Maximum number of commits to retrieve
        
    Returns:
        list: List of commit message strings
    """
    commits = get_commit_history(repo_path, file_path, limit)
    return [commit['message'] for commit in commits]


def summarize_commits_with_ai(
    commit_messages: List[str],
    model: str = DEFAULT_MODEL
) -> str:
    """
    Use an LLM to summarize a list of commit messages.
    
    Args:
        commit_messages: List of commit message strings
        model: OpenAI model to use
        
    Returns:
        str: AI-generated summary of the commits
        
    Example:
        >>> messages = ['Fixed bug in parser', 'Added error handling', 'Updated tests']
        >>> summary = summarize_commits_with_ai(messages)
        >>> print(summary)
    """
    if not commit_messages:
        return "No recent changes found for this file."
    
    if not client:
        return "Recent changes available but AI summarization is disabled (no API key)."
    
    # Format commit messages
    formatted_commits = "\n".join([f"- {msg}" for msg in commit_messages])
    
    prompt = f"""You are a technical project manager summarizing code changes.

Given the following git commit messages for a Python file, create a concise 2-3 sentence 
summary of the recent changes in plain English. Focus on what was changed and why, 
suitable for a documentation website's "Recent Changes" section.

Be professional and informative. Do not use phrases like "the commits show" or "according to the messages".
Just state what was done directly.

Commit messages:
{formatted_commits}

Summary:"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical writer specializing in clear, concise summaries of code changes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=200
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"Error summarizing commits: {e}")
        return "Could not generate summary of recent changes."


def get_file_summary(
    repo_path: str,
    file_path: str,
    limit: int = 5
) -> str:
    """
    Get an AI-generated summary of recent changes for a file.
    
    This is a convenience function that combines get_commit_messages
    and summarize_commits_with_ai.
    
    Args:
        repo_path: Path to the git repository root
        file_path: Path to the file
        limit: Maximum number of commits to analyze
        
    Returns:
        str: AI-generated summary of recent changes
    """
    messages = get_commit_messages(repo_path, file_path, limit)
    return summarize_commits_with_ai(messages)


def get_repository_info(repo_path: str) -> dict:
    """
    Get general information about a git repository.
    
    Args:
        repo_path: Path to the git repository
        
    Returns:
        dict: Repository information including branch, remote, and commit count
    """
    try:
        repo = Repo(repo_path)
        
        # Get current branch
        current_branch = repo.active_branch.name if not repo.head.is_detached else "detached"
        
        # Get remote URL
        remote_url = None
        if repo.remotes:
            remote_url = repo.remotes.origin.url if 'origin' in [r.name for r in repo.remotes] else repo.remotes[0].url
        
        # Get total commit count
        commit_count = sum(1 for _ in repo.iter_commits())
        
        # Get last commit
        last_commit = repo.head.commit
        
        return {
            'branch': current_branch,
            'remote_url': remote_url,
            'commit_count': commit_count,
            'last_commit': {
                'message': last_commit.message.strip(),
                'author': last_commit.author.name,
                'date': datetime.fromtimestamp(last_commit.committed_date).strftime('%Y-%m-%d %H:%M'),
                'hash': last_commit.hexsha[:7]
            }
        }
        
    except Exception as e:
        print(f"Error getting repository info: {e}")
        return {}


def format_commit_history(commits: List[dict]) -> str:
    """
    Format commit history as a readable string.
    
    Args:
        commits: List of commit dictionaries from get_commit_history
        
    Returns:
        str: Formatted commit history
    """
    if not commits:
        return "No commit history available."
    
    lines = ["Recent Commits:", ""]
    for commit in commits:
        lines.append(f"- **{commit['hash']}** ({commit['date']}) by {commit['author']}")
        lines.append(f"  {commit['message']}")
        lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        repo_path = "."
        
        print(f"\n📊 Analyzing git history for: {file_path}\n")
        
        # Check if it's a git repository
        if not is_git_repository(repo_path):
            print("❌ Not a git repository")
            sys.exit(1)
        
        # Get commit history
        commits = get_commit_history(repo_path, file_path, limit=5)
        
        if commits:
            print(format_commit_history(commits))
            print("\n" + "="*60 + "\n")
            
            # Get AI summary
            messages = [c['message'] for c in commits]
            summary = summarize_commits_with_ai(messages)
            print("📝 AI Summary:")
            print(summary)
        else:
            print("No commits found for this file.")
    else:
        # Show repository info
        repo_path = "."
        if is_git_repository(repo_path):
            info = get_repository_info(repo_path)
            print("\n📦 Repository Information:")
            print(f"Branch: {info.get('branch', 'unknown')}")
            print(f"Remote: {info.get('remote_url', 'none')}")
            print(f"Total commits: {info.get('commit_count', 0)}")
            if info.get('last_commit'):
                lc = info['last_commit']
                print(f"\nLast commit: {lc['hash']} by {lc['author']}")
                print(f"Date: {lc['date']}")
                print(f"Message: {lc['message']}")
        else:
            print("Not a git repository")
