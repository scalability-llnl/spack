# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import spack.config as spack_config
import spack.fetch_strategy as spack_fs
import spack.stage as spack_stage


@pytest.mark.parametrize('use_curl', [True, False])
def test_s3fetchstrategy_sans_url(use_curl):
    """Ensure constructor with no URL fails."""
    with spack_config.override('config:use_curl', use_curl):
        with pytest.raises(ValueError):
            spack_fs.S3FetchStrategy(None)


@pytest.mark.parametrize('use_curl', [True, False])
def test_s3fetchstrategy_bad_url(tmpdir, use_curl):
    """Ensure fetch with bad URL fails as expected."""
    testpath = str(tmpdir)

    with spack_config.override('config:use_curl', use_curl):
        fetcher = spack_fs.S3FetchStrategy(url='file:///does-not-exist')
        assert fetcher is not None

        with spack_stage.Stage(fetcher, path=testpath) as stage:
            assert stage is not None
            assert fetcher.archive_file is None
            with pytest.raises(spack_fs.FetchError):
                fetcher.fetch()


@pytest.mark.parametrize('use_curl', [True, False])
def test_s3fetchstrategy_downloaded(tmpdir, use_curl):
    """Ensure fetch with archive file already downloaded is a noop."""
    testpath = str(tmpdir)
    archive = os.path.join(testpath, 's3.tar.gz')

    with spack_config.override('config:use_curl', use_curl):
        class Archived_S3FS(spack_fs.S3FetchStrategy):
            @property
            def archive_file(self):
                return archive

        url = 's3:///{0}'.format(archive)
        fetcher = Archived_S3FS(url=url)
        with spack_stage.Stage(fetcher, path=testpath):
            fetcher.fetch()
