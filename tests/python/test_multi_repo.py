"""
Tests for the MultiRepoManager class
"""

from pathlib import Path
import pytest
from genesis_frontend.core.multi_repo import MultiRepoManager

@pytest.fixture
def multi_repo_manager(tmp_path: Path) -> MultiRepoManager:
    """Creates a temporary multi-repo manager for testing."""
    return MultiRepoManager(tmp_path)

def test_new_repo(multi_repo_manager: MultiRepoManager):
    """Tests creating a new repository."""
    repo = multi_repo_manager.new_repo("test-repo")
    assert repo.path.name == "test-repo"
    assert "test-repo" in multi_repo_manager.repos

def test_get_repo(multi_repo_manager: MultiRepoManager):
    """Tests getting a repository by name."""
    multi_repo_manager.new_repo("test-repo")
    repo = multi_repo_manager.get_repo("test-repo")
    assert repo is not None
    assert repo.path.name == "test-repo"

def test_get_all_repos(multi_repo_manager: MultiRepoManager):
    """Tests getting all managed repositories."""
    multi_repo_manager.new_repo("repo1")
    multi_repo_manager.new_repo("repo2")
    repos = multi_repo_manager.get_all_repos()
    assert set(repos.keys()) == {"repo1", "repo2"}
