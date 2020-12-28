# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Blitz(AutotoolsPackage):
    """N-dimensional arrays for C++"""
    homepage = "http://github.com/blitzpp/blitz"
    url = "https://github.com/blitzpp/blitz/archive/1.0.1.tar.gz"

    version('1.0.1', sha256='b62fc3f07b64b264307b01fec5e4f2793e09a68dcb5378984aedbc2e4b3adcef')
    version('1.0.0', sha256='79c06ea9a0585ba0e290c8140300e3ad19491c45c1d90feb52819abc3b58a0c1')

    build_targets = ['lib']

    def check(self):
        make('check-testsuite')
        make('check-examples')
