# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.fetch_strategy
import spack.stage


def test_gcsfetchstrategy_downloaded(tmp_path):
    """Ensure fetch with archive file already downloaded is a noop."""
    archive = tmp_path / "gcs.tar.gz"

    class Archived_GCSFS(spack.fetch_strategy.GCSFetchStrategy):
        @property
        def archive_file(self):
            return str(archive)

    fetcher = Archived_GCSFS(url="gs://example/gcs.tar.gz")
    with spack.stage.Stage(fetcher, path=str(tmp_path)):
        fetcher.fetch()
