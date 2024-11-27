# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.fetch_strategy as spack_fs
import spack.stage as spack_stage


def test_s3fetchstrategy_downloaded(tmp_path):
    """Ensure fetch with archive file already downloaded is a noop."""
    archive = tmp_path / "s3.tar.gz"

    class Archived_S3FS(spack_fs.S3FetchStrategy):
        @property
        def archive_file(self):
            return archive

    fetcher = Archived_S3FS(url="s3://example/s3.tar.gz")
    with spack_stage.Stage(fetcher, path=str(tmp_path)):
        fetcher.fetch()
