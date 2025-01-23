# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from pathlib import Path

import pytest

from llnl.util.filesystem import mkdirp, touch, working_dir

import spack.concretize
from spack.fetch_strategy import CvsFetchStrategy
from spack.stage import Stage
from spack.util.executable import which
from spack.version import Version

pytestmark = pytest.mark.skipif(not which("cvs"), reason="requires CVS to be installed")


@pytest.mark.parametrize("type_of_test", ["default", "branch", "date"])
def test_fetch(type_of_test, mock_cvs_repository, config, mutable_mock_repo):
    """Tries to:

    1. Fetch the repo using a fetch strategy constructed with
       supplied args (they depend on type_of_test).
    2. Check whether the checkout is on the correct branch or date
    3. Check if the test_file is in the checked out repository.
    4. Add and remove some files, then reset the repo, and
       ensure it's all there again.

    CVS does not have the notion of a unique branch; branches and revisions
    are managed separately for every file.
    """
    # Retrieve the right test parameters
    test = mock_cvs_repository.checks[type_of_test]
    get_branch = mock_cvs_repository.get_branch
    get_date = mock_cvs_repository.get_date

    # Construct the package under test
    spec = spack.concretize.concretize_one("cvs-test")
    spec.package.versions[Version("cvs")] = test.args

    # Enter the stage directory and check some properties
    with spec.package.stage:
        spec.package.do_stage()

        with working_dir(spec.package.stage.source_path):
            # Check branch
            if test.branch is not None:
                assert get_branch() == test.branch

            # Check date
            if test.date is not None:
                assert get_date() <= test.date

            source_path = Path(spec.package.stage.source_path)
            file_path = source_path / test.file
            assert source_path.is_dir()
            assert file_path.is_file()

            file_path.unlink()
            assert not file_path.is_file()

            untracked_file = Path("foobarbaz")
            touch(untracked_file)
            assert untracked_file.is_file()
            spec.package.do_restage()
            assert not untracked_file.is_file()

            assert source_path.is_dir()
            assert file_path.is_file()


def test_cvs_extra_fetch(tmpdir):
    """Ensure a fetch after downloading is effectively a no-op."""
    testpath = str(tmpdir)

    fetcher = CvsFetchStrategy(cvs=":pserver:not-a-real-cvs-repo%module=not-a-real-module")
    assert fetcher is not None

    with Stage(fetcher, path=testpath) as stage:
        assert stage is not None

        source_path = stage.source_path
        mkdirp(source_path)

        # TODO: This doesn't look as if it was testing what this function's
        # comment says it is testing. However, the other `test_*_extra_fetch`
        # functions (for svn, git, hg) use equivalent code.
        #
        # We're calling `fetcher.fetch` twice as this might be what we want to
        # do, and it can't hurt. See
        # <https://github.com/spack/spack/pull/23212> for a discussion on this.

        # Fetch once
        fetcher.fetch()
        # Fetch a second time
        fetcher.fetch()
