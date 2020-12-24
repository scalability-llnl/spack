# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import spack.main
from spack.spec import Spec


fetch = spack.main.SpackCommand('fetch')


@pytest.mark.disable_clean_stage_check
def test_fetch(mock_packages, config):

    cspec = Spec('corge')
    cspec.concretize()

    gspec = Spec('garply')
    gspec.concretize()

    output = fetch('-D', 'corge')

    assert cspec.package.url in output
    assert gspec.package.url in output

    assert os.path.exists(cspec.package.stage.archive_file)
    assert os.path.exists(gspec.package.stage.archive_file)


@pytest.mark.disable_clean_stage_check
def test_fetch_missing(mock_packages, config):

    qspec = Spec('quux')
    qspec.concretize()
    gspec = Spec('garply')
    gspec.concretize()

    fetch('quux')

    output = fetch('-m', 'corge')

    assert qspec.package.url not in output
    assert os.path.exists(qspec.package.stage.archive_file)
    assert os.path.exists(gspec.package.stage.archive_file)
