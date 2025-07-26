"""
Repository management for Genesis Frontend

This module provides a Repo class to abstract repository operations.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional


class Repo:
    """Represents a repository."""

    def __init__(self, path: Path):
        self.path = path

    def add_file(self, file_path: str, content: str) -> None:
        """Adds a file to the repository."""
        full_path = self.path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")

    def get_file_content(self, file_path: str) -> str:
        """Returns the content of a file."""
        return (self.path / file_path).read_text(encoding="utf-8")

    def list_files(self) -> List[str]:
        """Returns a list of all files in the repository."""
        return [
            str(p.relative_to(self.path))
            for p in self.path.rglob("*")
            if p.is_file()
        ]

    @classmethod
    def from_scratch(cls, path: Path) -> Repo:
        """Create a new repository from scratch."""
        path.mkdir(parents=True, exist_ok=True)
        return cls(path)
