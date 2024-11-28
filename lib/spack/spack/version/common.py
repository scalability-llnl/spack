# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import spack.error

# regex for a commit version
COMMIT_VERSION = re.compile(r"^[a-f0-9]{40}$")

# Infinity-like versions. The order in the list implies the comparison rules
infinity_versions = ["stable", "trunk", "head", "master", "main", "develop"]

iv_min_len = min(len(s) for s in infinity_versions)

ALPHA = 0
BETA = 1
RC = 2
FINAL = 3

PRERELEASE_TO_STRING = ["alpha", "beta", "rc"]
STRING_TO_PRERELEASE = {"alpha": ALPHA, "beta": BETA, "rc": RC, "final": FINAL}


def is_git_version(string: str) -> bool:
    return (
        string.startswith("git.")
        or len(string) == 40
        and bool(COMMIT_VERSION.match(string))
        or "=" in string[1:]
    )


class VersionError(spack.error.SpackError):
    """This is raised when something is wrong with a version."""


class VersionChecksumError(VersionError):
    """Raised for version checksum errors."""


class VersionLookupError(VersionError):
    """Raised for errors looking up git commits as versions."""


class EmptyRangeError(VersionError):
    """Raised when constructing an empty version range."""
