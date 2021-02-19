# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

from spack.main import SpackCommand
from spack.spec import Spec

stage = SpackCommand('stage')


@pytest.mark.disable_clean_stage_check
def test_stage_cmd(mock_packages, mock_fetch, config,
                   install_mockery):

    spec = Spec('patchcmd')
    spec.concretize()
    stage('patchcmd')

    path = spec.package.stage.source_path

    assert os.path.exists(os.path.join(path, 'configure'))


@pytest.mark.disable_clean_stage_check
def test_stage_path(tmpdir, mock_packages, mock_fetch, config,
                    install_mockery):

    test = os.path.join(tmpdir.strpath, 'test')
    spec = Spec('patchcmd')
    spec.concretize()

    stage('-p', str(test), 'patchcmd')

    assert os.path.exists(os.path.join(test, 'spack-src', 'configure'))
