# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Caches used by Spack to store data"""
import os
from pathlib import Path, PurePath

import llnl.util.lang
from llnl.util.filesystem import mkdirp
from llnl.util.symlink import symlink

import spack.config
import spack.error
import spack.fetch_strategy
import spack.paths
import spack.util.file_cache
import spack.util.path


def misc_cache_location():
    """The ``misc_cache`` is Spack's cache for small data.

    Currently the ``misc_cache`` stores indexes for virtual dependency
    providers and for which packages provide which tags.
    """
    path = spack.config.get("config:misc_cache", spack.paths.default_misc_cache_path)
    return spack.util.path.canonicalize_path(path)


def _misc_cache():
    path = misc_cache_location()
    return spack.util.file_cache.FileCache(path)


#: Spack's cache for small data
misc_cache = llnl.util.lang.Singleton(_misc_cache)


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


class MirrorCache(object):
    def __init__(self, root, skip_unstable_versions):
        self.root = Path(root).resolve()
        self.skip_unstable_versions = skip_unstable_versions

    def store(self, fetcher, relative_dest):
        """Fetch and relocate the fetcher's target into our mirror cache."""

        # Note this will archive package sources even if they would not
        # normally be cached (e.g. the current tip of an hg/git branch)
        dst = PurePath(self.root, relative_dest)
        mkdirp(PurePath(dst).parent)
        fetcher.archive(dst)

    def symlink(self, mirror_ref):
        """Symlink a human readible path in our mirror to the actual
        storage location."""

        cosmetic_path = PurePath(self.root, mirror_ref.cosmetic_path)
        storage_path = PurePath(self.root, mirror_ref.storage_path)
        relative_dst = os.path.relpath(storage_path, start=PurePath(cosmetic_path).parent)

        if not Path(cosmetic_path).exists():
            if os.path.lexists(cosmetic_path):
                # In this case the link itself exists but it is broken: remove
                # it and recreate it (in order to fix any symlinks broken prior
                # to https://github.com/spack/spack/pull/13908)
                Path(cosmetic_path).unlink()
            mkdirp(PurePath(cosmetic_path).parent)
            symlink(relative_dst, cosmetic_path)


#: Spack's local cache for downloaded source archives
fetch_cache = llnl.util.lang.Singleton(_fetch_cache)
