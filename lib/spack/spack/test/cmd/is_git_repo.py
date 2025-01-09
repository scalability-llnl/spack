# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

from llnl.util.filesystem import mkdirp, working_dir

import spack
import spack.cmd
import spack.fetch_strategy
from spack.version import ver


@pytest.fixture(scope="function")
def git_tmp_worktree(git, tmpdir, mock_git_version_info):
    """Create new worktree in a temporary folder and monkeypatch
    spack.paths.prefix to point to it.
    """

    # We need `git worktree remove` for this fixture, which was added in 2.17.0.
    # See https://github.com/git/git/commit/cc73385cf6c5c229458775bc92e7dbbe24d11611
    git_version = spack.fetch_strategy.GitFetchStrategy.version_from_git(git)
    if git_version < ver("2.17.0"):
        pytest.skip("git_tmp_worktree requires git v2.17.0")

    with working_dir(mock_git_version_info[0]):
        # TODO: This is fragile and should be high priority for
        # follow up fixes. 27021
        # Path length is occasionally too long on Windows
        # the following reduces the path length to acceptable levels
        if sys.platform == "win32":
            long_pth = str(tmpdir).split(os.path.sep)
            tmp_worktree = os.path.sep.join(long_pth[:-1])
        else:
            tmp_worktree = str(tmpdir)
        worktree_root = os.path.sep.join([tmp_worktree, "wrktree"])

        mkdirp(worktree_root)

        git("worktree", "add", "--detach", worktree_root, "HEAD")

        yield worktree_root

        git("worktree", "remove", "--force", worktree_root)


def test_is_git_repo_in_worktree(git_tmp_worktree):
    """Verify that spack.cmd.spack_is_git_repo() can identify a git repository
    in a worktree.
    """
    assert spack.cmd.is_git_repo(git_tmp_worktree)


def test_spack_is_git_repo_nongit(tmpdir, monkeypatch):
    """Verify that spack.cmd.spack_is_git_repo() correctly returns False if we
    are in a non-git directory.
    """
    assert not spack.cmd.is_git_repo(str(tmpdir))
