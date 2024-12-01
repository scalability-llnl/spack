# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

from llnl.util.filesystem import mkdirp, touch

import spack.config
import spack.util.url as url_util
from spack.fetch_strategy import CacheURLFetchStrategy, NoCacheError
from spack.stage import Stage


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_fetch_missing_cache(tmpdir, _fetch_method):
    """Ensure raise a missing cache file."""
    testpath = str(tmpdir)
    non_existing = os.path.join(testpath, "non-existing")
    with spack.config.override("config:url_fetch_method", _fetch_method):
        url = url_util.path_to_file_url(non_existing)
        fetcher = CacheURLFetchStrategy(url=url)
        with Stage(fetcher, path=testpath):
            with pytest.raises(NoCacheError, match=r"No cache"):
                fetcher.fetch()


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_fetch(tmpdir, _fetch_method):
    """Ensure a fetch after expanding is effectively a no-op."""
    cache_dir = tmpdir.join("cache")
    stage_dir = tmpdir.join("stage")
    mkdirp(cache_dir)
    mkdirp(stage_dir)
    cache = os.path.join(cache_dir, "cache.tar.gz")
    touch(cache)
    url = url_util.path_to_file_url(cache)
    with spack.config.override("config:url_fetch_method", _fetch_method):
        fetcher = CacheURLFetchStrategy(url=url)
        with Stage(fetcher, path=str(stage_dir)) as stage:
            source_path = stage.source_path
            mkdirp(source_path)
            fetcher.fetch()
