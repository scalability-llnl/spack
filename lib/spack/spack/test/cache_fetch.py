# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from pathlib import Path, PurePath

import pytest

from llnl.util.filesystem import mkdirp, touch

import spack.config
import spack.util.url as url_util
from spack.fetch_strategy import CacheURLFetchStrategy, NoCacheError
from spack.stage import Stage


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_fetch_missing_cache(tmp_path, _fetch_method):
    """Ensure raise a missing cache file."""
    non_existing = tmp_path / "non-existing"
    with spack.config.override("config:url_fetch_method", _fetch_method):
        url = url_util.path_to_file_url(non_existing)
        fetcher = CacheURLFetchStrategy(url=url)
        with Stage(fetcher, path=str(tmp_path)):
            with pytest.raises(NoCacheError, match=r"No cache"):
                fetcher.fetch()


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_fetch(tmp_path, _fetch_method):
    """Ensure a fetch after expanding is effectively a no-op."""
    cache_dir = tmp_path / "cache"
    stage_dir = tmp_path / "stage"
    mkdirp(cache_dir)
    mkdirp(stage_dir)
    cache = cache_dir / "cache.tar.gz"
    touch(cache)
    url = url_util.path_to_file_url(cache)
    with spack.config.override("config:url_fetch_method", _fetch_method):
        fetcher = CacheURLFetchStrategy(url=url)
        with Stage(fetcher, path=str(stage_dir)) as stage:
            source_path = stage.source_path
            mkdirp(source_path)
            fetcher.fetch()
