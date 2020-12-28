# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Faust(MakefilePackage):
    """Faust (Functional Audio Stream) is a functional programming language
    specifically designed for real-time signal processing and synthesis.
    A distinctive characteristic of Faust is to be fully compiled."""

    homepage = "http://faust.grame.fr/"
    url      = "https://github.com/grame-cncm/faust/archive/2.27.2.tar.gz"

    version('2.27.2', sha256='3367a868a93b63582bae29ab8783f1df7a10f4084a2bc1d2258ebf3d6a8c31d7')
    version('2.27.1', sha256='b3e93ca573025b231931e5eb92efc1a1e7f7720902aa3b285061519600a8c417')

    depends_on('cmake', type='build')

    def install(self, spec, prefix):
        make('PREFIX={0}'.format(prefix), 'install')
