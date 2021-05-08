# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

from llnl.util.filesystem import touch, working_dir, mkdirp

import spack.repo
import spack.config
from spack.spec import Spec
from spack.stage import Stage
from spack.version import ver
from spack.fetch_strategy import CvsFetchStrategy
from spack.util.executable import which


pytestmark = pytest.mark.skipif(
    not which('cvs'),
    reason='requires CVS to be installed')


@pytest.mark.parametrize("type_of_test", ['default'])
def test_fetch(
        type_of_test,
        mock_cvs_repository,
        config,
        mutable_mock_repo
):
    """Tries to:

    1. Fetch the repo using a fetch strategy constructed with
       supplied args (they depend on type_of_test).
    2. Check if the test_file is in the checked out repository.
    3. Add and remove some files, then reset the repo, and
       ensure it's all there again.

    CVS does not have the notion of a unique branch; branches and revisions
    are managed separately for every file.
    """
    # Retrieve the right test parameters
    t = mock_cvs_repository.checks[type_of_test]

    # Construct the package under test
    spec = Spec('cvs-test')
    spec.concretize()
    pkg = spack.repo.get(spec)
    pkg.versions[ver('cvs')] = t.args

    # Enter the stage directory and check some properties
    with pkg.stage:
        pkg.do_stage()

        with working_dir(pkg.stage.source_path):
            file_path = os.path.join(pkg.stage.source_path, t.file)
            assert os.path.isdir(pkg.stage.source_path)
            assert os.path.isfile(file_path)

            os.unlink(file_path)
            assert not os.path.isfile(file_path)

            untracked_file = 'foobarbaz'
            touch(untracked_file)
            assert os.path.isfile(untracked_file)
            pkg.do_restage()
            assert not os.path.isfile(untracked_file)

            assert os.path.isdir(pkg.stage.source_path)
            assert os.path.isfile(file_path)


def test_cvs_extra_fetch(tmpdir):
    """Ensure a fetch after downloading is effectively a no-op."""
    testpath = str(tmpdir)

    fetcher = CvsFetchStrategy(
        cvs=':pserver:not-a-real-cvs-repo%module=not-a-real-module')
    assert fetcher is not None

    with Stage(fetcher, path=testpath) as stage:
        assert stage is not None

        source_path = stage.source_path
        mkdirp(source_path)

        fetcher.fetch()
