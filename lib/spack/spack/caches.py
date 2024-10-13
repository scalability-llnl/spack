# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Caches used by Spack to store data"""
import os
from typing import Union

import llnl.util.lang
from llnl.util.filesystem import mkdirp

import spack.config
import spack.fetch_strategy
import spack.paths
import spack.util.file_cache
import spack.util.path


def misc_cache_location():
    """The ``MISC_CACHE`` is Spack's cache for small data.

    Currently the ``MISC_CACHE`` stores indexes for virtual dependency
    providers and for which packages provide which tags.
    """
    path = spack.config.get("config:misc_cache", spack.paths.default_misc_cache_path)
    return spack.util.path.canonicalize_path(path)


def _misc_cache():
    path = misc_cache_location()
    return spack.util.file_cache.FileCache(path)


FileCacheType = Union[spack.util.file_cache.FileCache, llnl.util.lang.Singleton]

#: Spack's cache for small data
MISC_CACHE: Union[spack.util.file_cache.FileCache, llnl.util.lang.Singleton] = (
    llnl.util.lang.Singleton(_misc_cache)
)


def fetch_cache_location():
    """Filesystem cache of downloaded archives.

    This prevents Spack from repeatedly fetch the same files when
    building the same package different ways or multiple times.
    """
    path = spack.config.get("config:source_cache")
    if not path:
        path = spack.paths.default_fetch_cache_path
    path = spack.util.path.canonicalize_path(path)
    return path


def _fetch_cache():
    path = fetch_cache_location()
    return spack.fetch_strategy.FsCache(path)


class MirrorCache:
    def __init__(self, root, skip_unstable_versions):
        self.root = os.path.abspath(root)
        self.skip_unstable_versions = skip_unstable_versions

    def store(self, fetcher, relative_dest):
        """Fetch and relocate the fetcher's target into our mirror cache."""

        # Note this will archive package sources even if they would not
        # normally be cached (e.g. the current tip of an hg/git branch)
        dst = os.path.join(self.root, relative_dest)
        mkdirp(os.path.dirname(dst))
        fetcher.archive(dst)


#: Spack's local cache for downloaded source archives
FETCH_CACHE: Union[spack.fetch_strategy.FsCache, llnl.util.lang.Singleton] = (
    llnl.util.lang.Singleton(_fetch_cache)
)
