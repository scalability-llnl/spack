# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand, SpackCommandError

info = SpackCommand('build-env')


@pytest.mark.parametrize('pkg', [
    ('zlib',)
])
@pytest.mark.usefixtures('config')
def test_it_just_runs(pkg):
    info(*pkg)


@pytest.mark.parametrize('pkg,error_cls', [
    ('zlib libszip', SpackCommandError),
    ('', IndexError)
])
@pytest.mark.usefixtures('config')
def test_it_just_fails(pkg, error_cls):
    with pytest.raises(error_cls):
        info(pkg)
