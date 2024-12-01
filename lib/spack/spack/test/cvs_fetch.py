# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

from llnl.util.filesystem import mkdirp, touch, working_dir

from spack.fetch_strategy import CvsFetchStrategy
from spack.spec import Spec
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
    spec = Spec("cvs-test").concretized()
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

            file_path = os.path.join(spec.package.stage.source_path, test.file)
            assert os.path.isdir(spec.package.stage.source_path)
            assert os.path.isfile(file_path)

            os.unlink(file_path)
            assert not os.path.isfile(file_path)

            untracked_file = "foobarbaz"
            touch(untracked_file)
            assert os.path.isfile(untracked_file)
            spec.package.do_restage()
            assert not os.path.isfile(untracked_file)

            assert os.path.isdir(spec.package.stage.source_path)
            assert os.path.isfile(file_path)


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
