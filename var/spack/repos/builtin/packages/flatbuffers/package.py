# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flatbuffers(CMakePackage):
    """Memory Efficient Serialization Library
    """

    homepage = "http://google.github.io/flatbuffers/"
    url      = "https://github.com/google/flatbuffers/archive/v1.9.0.tar.gz"

    version('1.12.0', sha256='62f2223fb9181d1d6338451375628975775f7522185266cd5296571ac152bc45')
    version('1.11.0', sha256='3f4a286642094f45b1b77228656fbd7ea123964f19502f9ecfd29933fd23a50b')
    version('1.10.0', sha256='3714e3db8c51e43028e10ad7adffb9a36fc4aa5b1a363c2d0c4303dd1be59a7c')
    version('1.9.0', sha256='5ca5491e4260cacae30f1a5786d109230db3f3a6e5a0eb45d0d0608293d247e3')
    version('1.8.0', sha256='c45029c0a0f1a88d416af143e34de96b3091642722aa2d8c090916c6d1498c2e')

    variant('shared', default=True,
            description='Build shared instead of static libraries')

    def cmake_args(self):
        args = []
        args.append('-DFLATBUFFERS_BUILD_SHAREDLIB={0}'.format(
            'ON' if '+shared' in self.spec else 'OFF'))
        args.append('-DFLATBUFFERS_BUILD_FLATLIB={0}'.format(
            'ON' if '+shared' not in self.spec else 'OFF'))
        if 'darwin' in self.spec.architecture:
            args.append('-DCMAKE_MACOSX_RPATH=ON')
        return args
