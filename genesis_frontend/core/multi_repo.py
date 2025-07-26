"""
Multi-repository management for Genesis Frontend
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from .repo import Repo


class MultiRepoManager:
    """Manages multiple repositories."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.repos: Dict[str, Repo] = {}

    def new_repo(self, name: str) -> Repo:
        """Creates a new repository."""
        repo_path = self.base_path / name
        repo = Repo.from_scratch(repo_path)
        self.repos[name] = repo
        return repo

    def get_repo(self, name: str) -> Optional[Repo]:
        """Returns a repository by name."""
        return self.repos.get(name)

    def get_all_repos(self) -> Dict[str, Repo]:
        """Returns all managed repositories."""
        return self.repos
