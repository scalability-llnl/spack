# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.spec
import spack.main

autoremove = spack.main.SpackCommand('autoremove')


@pytest.mark.db
def test_no_packages_to_remove(config, mutable_database, capsys):
    with capsys.disabled():
        output = autoremove('-y')
    assert 'There are no unused specs.' in output


@pytest.mark.db
def test_packages_are_removed(config, mutable_database, capsys):
    s = spack.spec.Spec('simple-inheritance')
    s.concretize()
    s.package.do_install(fake=True, explicit=True)
    with capsys.disabled():
        output = autoremove('-y')
    assert 'Successfully uninstalled cmake' in output
