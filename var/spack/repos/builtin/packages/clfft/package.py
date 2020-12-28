# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Clfft(CMakePackage):
    """a software library containing FFT functions written in OpenCL"""

    homepage = "https://github.com/clMathLibraries/clFFT"
    url      = "https://github.com/clMathLibraries/clFFT/archive/v2.12.2.tar.gz"

    version('2.12.2', sha256='e7348c146ad48c6a3e6997b7702202ad3ee3b5df99edf7ef00bbacc21e897b12')

    variant('client', default=True,
            description='build client and callback client')

    depends_on('opencl@1.2:')
    depends_on('boost@1.33.0:', when='+client')

    patch('https://github.com/clMathLibraries/clFFT/commit/eea7dbc888367b8dbea602ba539eb1a9cbc118d9.patch',
          sha256='3148d5937077def301b30b913bc2437df869204fca1de4385ccd46e3b98b13aa', when='@2.12.2')

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_CLIENT:BOOL={0}'.format((
                'ON' if '+client' in spec else 'OFF')),
            '-DBUILD_CALLBACK_CLIENT:BOOL={0}'.format((
                'ON' if '+client' in spec else 'OFF'))
        ]
        return args
