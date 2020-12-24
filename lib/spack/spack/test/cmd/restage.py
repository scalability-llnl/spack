# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

from llnl.util.filesystem import working_dir

from spack.util.executable import Executable
from spack.main import SpackCommand
from spack.spec import Spec


restage = SpackCommand('restage')
patch = SpackCommand('patch')


@pytest.mark.disable_clean_stage_check
def test_restage_cmd(mock_packages, mock_fetch, config,
                     install_mockery):

    spec = Spec('patchcmd')
    spec.concretize()
    patch('patchcmd')

    with working_dir(spec.package.stage.source_path):
        configure = Executable('./configure')
        configure()

        with open('Makefile') as mf:
            assert 'Patchcmd!' in mf.read()

    restage('patchcmd')
    path = spec.package.stage.source_path

    assert not os.path.exists(os.path.join(path, 'Makefile'))
