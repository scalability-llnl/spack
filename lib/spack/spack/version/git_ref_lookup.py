# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

from llnl.util.filesystem import mkdirp, working_dir

import spack.caches
import spack.fetch_strategy
import spack.paths
import spack.repo
import spack.util.executable
import spack.util.hash
import spack.util.spack_json as sjson

from .common import VersionLookupError
from .lookup import AbstractRefLookup

# regular expression for semantic versioning
_VERSION_CORE = r"\d+\.\d+\.\d+"
_IDENT = r"[0-9A-Za-z-]+"
_SEPARATED_IDENT = rf"{_IDENT}(?:\.{_IDENT})*"
_PRERELEASE = rf"\-{_SEPARATED_IDENT}"
_BUILD = rf"\+{_SEPARATED_IDENT}"
_SEMVER = rf"{_VERSION_CORE}(?:{_PRERELEASE})?(?:{_BUILD})?"

# clamp on the end, so versions like v1.2.3-rc1 will match
# without the leading 'v'.
SEMVER_REGEX = re.compile(rf"{_SEMVER}$")


class GitRefLookup(AbstractRefLookup):
    """An object for cached lookups of git refs

    GitRefLookup objects delegate to the MISC_CACHE for locking. GitRefLookup objects may
    be attached to a GitVersion to allow for comparisons between git refs and versions as
    represented by tags in the git repository.
    """

    def __init__(self, pkg_name):
        self.pkg_name = pkg_name

        self.data: Dict[str, Tuple[Optional[str], int]] = {}

        self._pkg = None
        self._fetcher = None
        self._cache_key = None
        self._cache_path = None

    # The following properties are used as part of a lazy reference scheme
    # to avoid querying the package repository until it is necessary (and
    # in particular to wait until after the configuration has been
    # assembled)
    @property
    def cache_key(self):
        if not self._cache_key:
            key_base = "git_metadata"
            self._cache_key = (Path(key_base) / self.repository_uri).as_posix()

            # Cache data in MISC_CACHE
            # If this is the first lazy access, initialize the cache as well
            spack.caches.MISC_CACHE.init_entry(self.cache_key)
        return self._cache_key

    @property
    def cache_path(self):
        if not self._cache_path:
            self._cache_path = spack.caches.MISC_CACHE.cache_path(self.cache_key)
        return self._cache_path

    @property
    def pkg(self):
        if not self._pkg:
            try:
                pkg = spack.repo.PATH.get_pkg_class(self.pkg_name)
                pkg.git
            except (spack.repo.RepoError, AttributeError) as e:
                raise VersionLookupError(f"Couldn't get the git repo for {self.pkg_name}") from e
            self._pkg = pkg
        return self._pkg

    @property
    def fetcher(self):
        if not self._fetcher:
            # We require the full git repository history
            fetcher = spack.fetch_strategy.GitFetchStrategy(git=self.pkg.git)
            fetcher.get_full_repo = True
            self._fetcher = fetcher
        return self._fetcher

    @property
    def repository_uri(self):
        """Identifier for git repos used within the repo and metadata caches."""
        return Path(spack.util.hash.b32_hash(self.pkg.git)[-7:])

    def save(self):
        """Save the data to file"""
        with spack.caches.MISC_CACHE.write_transaction(self.cache_key) as (old, new):
            sjson.dump(self.data, new)

    def load_data(self):
        """Load data if the path already exists."""
        if os.path.isfile(self.cache_path):
            with spack.caches.MISC_CACHE.read_transaction(self.cache_key) as cache_file:
                self.data = sjson.load(cache_file)

    def get(self, ref) -> Tuple[Optional[str], int]:
        if not self.data:
            self.load_data()

        if ref not in self.data:
            self.data[ref] = self.lookup_ref(ref)
            self.save()

        return self.data[ref]

    def lookup_ref(self, ref) -> Tuple[Optional[str], int]:
        """Lookup the previous version and distance for a given commit.

        We use git to compare the known versions from package to the git tags,
        as well as any git tags that are SEMVER versions, and find the latest
        known version prior to the commit, as well as the distance from that version
        to the commit in the git repo. Those values are used to compare Version objects.
        """
        pathlib_dest = Path(spack.paths.user_repos_cache_path) / self.repository_uri
        dest = str(pathlib_dest)

        # prepare a cache for the repository
        dest_parent = os.path.dirname(dest)
        if not os.path.exists(dest_parent):
            mkdirp(dest_parent)

        # Only clone if we don't have it!
        if not os.path.exists(dest):
            self.fetcher.bare_clone(dest)

        # Lookup commit info
        with working_dir(dest):
            # TODO: we need to update the local tags if they changed on the
            # remote instance, simply adding '-f' may not be sufficient
            # (if commits are deleted on the remote, this command alone
            # won't properly update the local rev-list)
            self.fetcher.git("fetch", "--tags", output=os.devnull, error=os.devnull)

            # Ensure ref is a commit object known to git
            # Note the brackets are literals, the ref replaces the format string
            try:
                self.fetcher.git(
                    "cat-file", "-e", "%s^{commit}" % ref, output=os.devnull, error=os.devnull
                )
            except spack.util.executable.ProcessError:
                raise VersionLookupError("%s is not a valid git ref for %s" % (ref, self.pkg_name))

            # List tags (refs) by date, so last reference of a tag is newest
            tag_info = self.fetcher.git(
                "for-each-ref",
                "--sort=creatordate",
                "--format",
                "%(objectname) %(refname)",
                "refs/tags",
                output=str,
            ).split("\n")

            # Lookup of commits to spack versions
            commit_to_version = {}

            for entry in tag_info:
                if not entry:
                    continue
                tag_commit, tag = entry.split()
                tag = tag.replace("refs/tags/", "", 1)

                # For each tag, try to match to a version
                for v in [v.string for v in self.pkg.versions]:
                    if v == tag or "v" + v == tag:
                        commit_to_version[tag_commit] = v
                        break
                else:
                    # try to parse tag to compare versions spack does not know
                    match = SEMVER_REGEX.search(tag)
                    if match:
                        commit_to_version[tag_commit] = match.group()

            ancestor_commits = []
            for tag_commit in commit_to_version:
                self.fetcher.git("merge-base", "--is-ancestor", tag_commit, ref, ignore_errors=[1])
                if self.fetcher.git.returncode == 0:
                    distance = self.fetcher.git(
                        "rev-list", "%s..%s" % (tag_commit, ref), "--count", output=str, error=str
                    ).strip()
                    ancestor_commits.append((tag_commit, int(distance)))

            if ancestor_commits:
                # Get nearest ancestor that is a known version
                prev_version_commit, distance = min(ancestor_commits, key=lambda x: x[1])
                prev_version = commit_to_version[prev_version_commit]
            else:
                # Get list of all commits, this is in reverse order
                # We use this to get the first commit below
                ref_info = self.fetcher.git("log", "--all", "--pretty=format:%H", output=str)
                commits = [c for c in ref_info.split("\n") if c]

                # No previous version and distance from first commit
                prev_version = None
                distance = int(
                    self.fetcher.git(
                        "rev-list", "%s..%s" % (commits[-1], ref), "--count", output=str, error=str
                    ).strip()
                )

        return prev_version, distance
