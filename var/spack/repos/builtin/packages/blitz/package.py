# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Blitz(AutotoolsPackage):
    """N-dimensional arrays for C++"""
    homepage = "http://github.com/blitzpp/blitz"
    url = "https://github.com/blitzpp/blitz/archive/1.0.2.tar.gz"

    version('1.0.2', sha256='500db9c3b2617e1f03d0e548977aec10d36811ba1c43bb5ef250c0e3853ae1c2')
    version('1.0.1', sha256='b62fc3f07b64b264307b01fec5e4f2793e09a68dcb5378984aedbc2e4b3adcef')
    version('1.0.0', sha256='79c06ea9a0585ba0e290c8140300e3ad19491c45c1d90feb52819abc3b58a0c1')

    depends_on('python@:2.7.999', type='build', when='@:1.0.1')
    depends_on('python@3:', type='build', when='@1.0.2:')

    build_targets = ['lib']

    def check(self):
        make('check-testsuite')
        make('check-examples')
