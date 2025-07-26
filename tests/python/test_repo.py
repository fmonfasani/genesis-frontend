"""
Tests for the Repo class
"""

from pathlib import Path
import pytest
from genesis_frontend.core.repo import Repo

@pytest.fixture
def repo(tmp_path: Path) -> Repo:
    """Creates a temporary repository for testing."""
    return Repo.from_scratch(tmp_path)

def test_add_file(repo: Repo):
    """Tests adding a file to the repository."""
    repo.add_file("test.txt", "hello")
    assert (repo.path / "test.txt").read_text() == "hello"

def test_get_file_content(repo: Repo):
    """Tests getting the content of a file."""
    (repo.path / "test.txt").write_text("hello")
    assert repo.get_file_content("test.txt") == "hello"

def test_list_files(repo: Repo):
    """Tests listing all files in the repository."""
    (repo.path / "a.txt").write_text("a")
    (repo.path / "b" / "c.txt").mkdir(parents=True)
    (repo.path / "b" / "c.txt").write_text("c")
    assert set(repo.list_files()) == {"a.txt", "b/c.txt"}
