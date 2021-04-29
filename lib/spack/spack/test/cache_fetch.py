# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

from llnl.util.filesystem import mkdirp, touch

import spack.config

from spack.stage import Stage
from spack.fetch_strategy import CacheURLFetchStrategy, NoCacheError


@pytest.mark.parametrize('use_curl', [True, False])
def test_fetch_missing_cache(tmpdir, use_curl):
    """Ensure raise a missing cache file."""
    testpath = str(tmpdir)
    with spack.config.override('config:use_curl', use_curl):
        fetcher = CacheURLFetchStrategy(url='file:///not-a-real-cache-file')
        with Stage(fetcher, path=testpath):
            with pytest.raises(NoCacheError, match=r'No cache'):
                fetcher.fetch()


@pytest.mark.parametrize('use_curl', [True, False])
def test_fetch(tmpdir, use_curl):
    """Ensure a fetch after expanding is effectively a no-op."""
    testpath = str(tmpdir)
    cache = os.path.join(testpath, 'cache.tar.gz')
    touch(cache)
    url = 'file:///{0}'.format(cache)
    with spack.config.override('config:use_curl', use_curl):
        fetcher = CacheURLFetchStrategy(url=url)
        with Stage(fetcher, path=testpath) as stage:
            source_path = stage.source_path
            mkdirp(source_path)
            fetcher.fetch()
