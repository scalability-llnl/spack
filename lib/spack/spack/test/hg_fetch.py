# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

from llnl.util.filesystem import mkdirp, touch, working_dir

import spack.config
from spack.fetch_strategy import HgFetchStrategy
from spack.spec import Spec
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
    s = Spec("hg-test").concretized()
    monkeypatch.setitem(s.package.versions, Version("hg"), t.args)

    # Enter the stage directory and check some properties
    with s.package.stage:
        with spack.config.override("config:verify_ssl", secure):
            s.package.do_stage()

        with working_dir(s.package.stage.source_path):
            assert h() == t.revision

            file_path = os.path.join(s.package.stage.source_path, t.file)
            assert os.path.isdir(s.package.stage.source_path)
            assert os.path.isfile(file_path)

            os.unlink(file_path)
            assert not os.path.isfile(file_path)

            untracked_file = "foobarbaz"
            touch(untracked_file)
            assert os.path.isfile(untracked_file)
            s.package.do_restage()
            assert not os.path.isfile(untracked_file)

            assert os.path.isdir(s.package.stage.source_path)
            assert os.path.isfile(file_path)

            assert h() == t.revision


def test_hg_extra_fetch(tmpdir):
    """Ensure a fetch after expanding is effectively a no-op."""
    testpath = str(tmpdir)

    fetcher = HgFetchStrategy(hg="file:///not-a-real-hg-repo")
    with Stage(fetcher, path=testpath) as stage:
        source_path = stage.source_path
        mkdirp(source_path)
        fetcher.fetch()
