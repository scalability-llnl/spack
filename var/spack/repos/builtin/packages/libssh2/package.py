# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libssh2(CMakePackage):
    """libssh2 is a client-side C library implementing the SSH2 protocol"""

    homepage = "https://www.libssh2.org/"
    url      = "https://www.libssh2.org/download/libssh2-1.7.0.tar.gz"

    version('1.9.0', sha256='d5fb8bd563305fd1074dda90bd053fb2d29fc4bce048d182f96eaa466dfadafd')
    version('1.8.2', sha256='088307d9f6b6c4b8c13f34602e8ff65d21c2dc4d55284dfe15d502c4ee190d67')
    version('1.8.1', sha256='40b517f35b1bb869d0075b15125c7a015557f53a5a3a6a8bffb89b69fd70f159')
    version('1.8.0', sha256='39f34e2f6835f4b992cafe8625073a88e5a28ba78f83e8099610a7b3af4676d4')
    version('1.7.0', sha256='e4561fd43a50539a8c2ceb37841691baf03ecb7daf043766da1b112e4280d584')
    version('1.4.3', sha256='eac6f85f9df9db2e6386906a6227eb2cd7b3245739561cad7d6dc1d5d021b96d')  # CentOS7

    variant('shared', default=True,
            description="Build shared libraries")

    depends_on('cmake@2.8.11:', type='build')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('xz')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_SHARED_LIBS=%s' % ('YES' if '+shared' in spec else 'NO')]

    @run_after('install')
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies('platform=darwin'):
            fix_darwin_install_name(self.prefix.lib)
