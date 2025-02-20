# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Single util module where Spack should get a git executable."""

import sys
from typing import Optional

import llnl.util.lang

import spack.util.executable as exe


@llnl.util.lang.memoized
def git(required: bool = False) -> Optional[exe.Executable]:
    """Get a git executable.

    Arguments:
        required: if ``True``, fail if ``git`` is not found. By default return ``None``.
    """
    git_exe: Optional[exe.Executable] = exe.which("git", required=required)

    # If we're running under pytest, add this to ignore the fix for CVE-2022-39253 in
    # git 2.38.1+. Do this in one place; we need git to do this in all parts of Spack.
    if git_exe and "pytest" in sys.modules:
        git_exe.add_default_arg("-c", "protocol.file.allow=always")

    return git_exe
