# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand
from spack.util.executable import which

pytestmark = pytest.mark.skipif(
    not which('git'), reason='requires git to be installed')

clone = SpackCommand('clone')


def test_clone(tmpdir):

    git = which('git', required=True)
    output = clone(str(tmpdir))

    with tmpdir.as_cwd():
        branch = git('branch', output=str).split()[1]

    assert "develop" == branch
    assert "Successfully created a new spack in" in output


def test_remote_clone(tmpdir, capfd):

    output = clone('-r', 'origin', str(tmpdir))

    assert "Successfully created a new spack in" in output
