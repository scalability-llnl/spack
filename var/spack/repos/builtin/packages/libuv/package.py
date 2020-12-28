# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libuv(AutotoolsPackage):
    """Multi-platform library with a focus on asynchronous IO"""
    homepage = "http://libuv.org"
    url = "https://github.com/libuv/libuv/archive/v1.9.0.tar.gz"

    version('1.40.0', sha256='70fe1c9ba4f2c509e8166c0ca2351000237da573bb6c82092339207a9715ba6b')
    version('1.39.0', sha256='dc7b21f1bb7ef19f4b42c5ea058afabe51132d165da18812b70fb319659ba629')
    version('1.38.1', sha256='2177fca2426ac60c20f654323656e843dac4f568d46674544b78f416697bd32c')
    version('1.25.0', sha256='ce3036d444c3fb4f9a9e2994bec1f4fa07872b01456998b422ce918fdc55c254')
    version('1.10.0', sha256='50f4ed57d65af4ab634e2cbdd90c49213020e15b4d77d3631feb633cbba9239f')
    version('1.9.0',  sha256='f8b8272a0d80138b709d38fad2baf771899eed61e7f9578d17898b07a1a2a5eb')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')

    # Tries to build an Objective-C file with GCC's C frontend
    # https://github.com/libuv/libuv/issues/2805
    conflicts('%gcc platform=darwin', when='@:1.37.9',
              msg='libuv does not compile with GCC on macOS yet, use clang. '
                  'See: https://github.com/libuv/libuv/issues/2805')

    def autoreconf(self, spec, prefix):
        # This is needed because autogen.sh generates on-the-fly
        # an m4 macro needed during configuration
        bash = which("bash")
        bash('autogen.sh')
