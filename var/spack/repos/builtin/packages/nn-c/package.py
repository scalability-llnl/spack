# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NnC(AutotoolsPackage):
    """nn: Natural Neighbours interpolation. nn is a C code
    for Natural Neighbours interpolation of 2D scattered data.
    It provides a C library and a command line utility nnbathy."""

    homepage = "https://github.com/sakov/nn-c"
    git      = "https://github.com/sakov/nn-c.git"

    version('master', branch='master')

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    configure_directory = 'nn'

    def configure_args(self):
        args = []
        if '+pic' in self.spec:
            args.extend([
                'CFLAGS={0}'.format(self.compiler.pic_flag),
                'CXXFLAGS={0}'.format(self.compiler.pic_flag),
                'FFLAGS={0}'.format(self.compiler.pic_flag)
            ])
        return args
