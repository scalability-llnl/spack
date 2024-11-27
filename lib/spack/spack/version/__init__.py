# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module implements Version and version-ish objects.  These are:

StandardVersion: A single version of a package.
ClosedOpenRange: A range of versions of a package.
VersionList: A ordered list of Version and VersionRange elements.

The set of Version and ClosedOpenRange is totally ordered wiht <
defined as Version(x) < VersionRange(Version(y), Version(x))
if Version(x) <= Version(y).
"""

from .common import (
    EmptyRangeError,
    VersionChecksumError,
    VersionError,
    VersionLookupError,
    infinity_versions,
    is_git_version,
)
from .version_types import (
    ClosedOpenRange,
    GitVersion,
    StandardVersion,
    Version,
    VersionList,
    VersionRange,
    _next_version,
    _prev_version,
    from_string,
    ver,
)

#: This version contains all possible versions.
any_version: VersionList = VersionList([":"])

__all__ = [
    "Version",
    "VersionRange",
    "ver",
    "from_string",
    "is_git_version",
    "infinity_versions",
    "_prev_version",
    "_next_version",
    "VersionList",
    "ClosedOpenRange",
    "StandardVersion",
    "GitVersion",
    "VersionError",
    "VersionChecksumError",
    "VersionLookupError",
    "EmptyRangeError",
    "any_version",
]
