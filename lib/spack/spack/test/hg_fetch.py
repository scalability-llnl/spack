# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from pathlib import Path

import pytest

from llnl.util.filesystem import mkdirp, touch, working_dir

import spack.concretize
import spack.config
from spack.fetch_strategy import HgFetchStrategy
from spack.stage import Stage
from spack.util.executable import which
from spack.version import Version

# Test functionality covered is supported on Windows, but currently failing
# and expected to be fixed
pytestmark = [
    pytest.mark.skipif(not which("hg"), reason="requires mercurial to be installed"),
    pytest.mark.not_on_windows("Failing on Win"),
]


@pytest.mark.parametrize("type_of_test", ["default", "rev0"])
@pytest.mark.parametrize("secure", [True, False])
def test_fetch(type_of_test, secure, mock_hg_repository, config, mutable_mock_repo, monkeypatch):
    """Tries to:

    1. Fetch the repo using a fetch strategy constructed with
       supplied args (they depend on type_of_test).
    2. Check if the test_file is in the checked out repository.
    3. Assert that the repository is at the revision supplied.
    4. Add and remove some files, then reset the repo, and
       ensure it's all there again.
    """
    # Retrieve the right test parameters
    t = mock_hg_repository.checks[type_of_test]
    h = mock_hg_repository.hash

    # Construct the package under test
    s = spack.concretize.concretize_one("hg-test")
    monkeypatch.setitem(s.package.versions, Version("hg"), t.args)

    # Enter the stage directory and check some properties
    with s.package.stage:
        with spack.config.override("config:verify_ssl", secure):
            s.package.do_stage()

        with working_dir(s.package.stage.source_path):
            assert h() == t.revision

            source_path = Path(s.package.stage.source_path)
            file_path = source_path / t.file
            assert source_path.is_dir()
            assert file_path.is_file()

            file_path.unlink()
            assert not file_path.is_file()

            untracked_file = Path("foobarbaz")
            touch(untracked_file)
            assert untracked_file.is_file()
            s.package.do_restage()
            assert not untracked_file.is_file()

            assert source_path.is_dir()
            assert file_path.is_file()

            assert h() == t.revision


def test_hg_extra_fetch(tmpdir):
    """Ensure a fetch after expanding is effectively a no-op."""
    testpath = str(tmpdir)

    fetcher = HgFetchStrategy(hg="file:///not-a-real-hg-repo")
    with Stage(fetcher, path=testpath) as stage:
        source_path = stage.source_path
        mkdirp(source_path)
        fetcher.fetch()
