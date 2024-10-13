# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
from typing import Optional

import spack.paths
import spack.util.git

#: PEP440 canonical <major>.<minor>.<micro>.<devN> string
__version__ = "0.23.0.dev0"
spack_version = __version__


def __try_int(v):
    try:
        return int(v)
    except ValueError:
        return v


#: (major, minor, micro, dev release) tuple
spack_version_info = tuple([__try_int(v) for v in __version__.split(".")])


def get_spack_commit() -> Optional[str]:
    """Get the Spack git commit sha.

    Returns:
        (str or None) the commit sha if available, otherwise None
    """
    git_path = os.path.join(spack.paths.prefix, ".git")
    if not os.path.exists(git_path):
        return None

    git = spack.util.git.git()
    if not git:
        return None

    rev = git(
        "-C",
        spack.paths.prefix,
        "rev-parse",
        "HEAD",
        output=str,
        error=os.devnull,
        fail_on_error=False,
    )
    if git.returncode != 0:
        return None

    match = re.match(r"[a-f\d]{7,}$", rev)
    return match.group(0) if match else None


def get_version() -> str:
    """Get a descriptive version of this instance of Spack.

    Outputs '<PEP440 version> (<git commit sha>)'.

    The commit sha is only added when available.
    """
    commit = get_spack_commit()
    if commit:
        return f"{spack_version} ({commit})"
    return spack_version


__all__ = ["spack_version_info", "spack_version", "get_version", "get_spack_commit"]
