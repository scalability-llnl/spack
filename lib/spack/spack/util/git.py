# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Single util module where Spack should get a git executable."""

import sys
from typing import List, Optional

import llnl.util.lang

import spack.util.executable as exe


@llnl.util.lang.memoized
def git(required: bool = False):
    """Get a git executable.

    Arguments:
        required: if ``True``, fail if ``git`` is not found. By default return ``None``.
    """
    git: Optional[exe.Executable] = exe.which("git", required=required)

    # If we're running under pytest, add this to ignore the fix for CVE-2022-39253 in
    # git 2.38.1+. Do this in one place; we need git to do this in all parts of Spack.
    if git and "pytest" in sys.modules:
        git.add_default_arg("-c", "protocol.file.allow=always")

    return git


def get_modified_files(from_ref: str = "HEAD~1", to_ref: str = "HEAD") -> List[str]:
    """Get a list of files modified between `from_ref` and `to_ref`
    Args:
       from_ref (str): oldest git ref, defaults to `HEAD~1`
       to_ref (str): newer git ref, defaults to `HEAD`
    Returns: list of file paths
    """
    git_exe = git(required=True)

    stdout = git_exe("diff", "--name-only", from_ref, to_ref, output=str)

    return stdout.split()
