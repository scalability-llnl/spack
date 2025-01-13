# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.repo
import spack.util.git
from .version_types import GitVersion, StandardVersion, Version
from spack.util.executable import ProcessError

from .common import COMMIT_VERSION


class GitBranch:
    def __init__(self, git_address, name):
        self.address = git_address
        self.name = name
        self.flag = "-h"


class GitTag:
    def __init__(self, git_address, name):
        self.address = git_address
        self.name = name
        self.flag = "-t"


def _associated_git_ref(version, package_class):
    """Retrieve the branch or tag associated with the version and return the relevant git information for querying the git repo/remote"""
    version_dict = package_class.versions.get(version, {})

    git_address = version_dict.get("git", None) or getattr(package_class, "git", None)

    if git_address:
        branch = version_dict.get("branch", None)
        tag = version_dict.get("tag", None)
        if branch:
            return GitBranch(git_address, branch)
        elif tag:
            return GitTag(git_address, tag)
    return None


def _retrieve_latest_git_hash(git_ref):
    """Get the git hash associated with a tag or branch"""
    # remote git operations can sometimes have banners so we must parse the output for a sha
    query = spack.util.git.git(required=True)(
        "ls-remote", git_ref.flag, git_ref.address, git_ref.name, output=str, error=os.devnull
    )
    sha, ref = query.strip().split()
    assert COMMIT_VERSION.match(sha)
    return sha


def convert_standard_to_git_version(version, package_class_name):
    """
    Converts a StandardVersion to a GitVersion

    This function will assign the Git commit sha to a version if it has a branch or tag
    """
    pkg_class = spack.repo.PATH.get_pkg_class(package_class_name)
    git_ref = _associated_git_ref(version, pkg_class)
    if git_ref:
        try:
            hash = _retrieve_latest_git_hash(git_ref)
        except (ProcessError, ValueError, AssertionError):
            raise InternalConcretizerError(
                (
                    "Failure to fetch git sha when running"
                    f" `git ls-remote {git_ref.address} {git_ref.name}`\n"
                    "Confirm network connectivty by running this command followed by:\n"
                    f"\t`spack fetch {git_ref.address}@{str(version)}`"
                    "Post a bug report if both of these operations succeed."
                )
            )

        new_version_str = f"git.{hash}={str(version)}"
        return GitVersion(new_version_str)
    else:
        return None


def maximally_resolved_version(version, package_class_name):
    """Transparent pass through of version conversion"""
    # ensure conversion
    version = Version(version)
    if isinstance(version, StandardVersion):
        new_version = convert_standard_to_git_version(version, package_class_name)
        if new_version:
            return new_version
        else:
            return version
    else:
        return version
