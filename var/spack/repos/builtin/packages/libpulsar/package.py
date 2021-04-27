# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libpulsar(CMakePackage):
    """libpulsar is a C/C++ client library implementation of the Apache Pulsar
     protocol."""

    homepage = "https://github.com/apache/pulsar"
    url      = "https://github.com/apache/pulsar/archive/v2.7.0.tar.gz"

    maintainers = ['aahmed-se']

    version('2.7.0',
            sha256='5bf8e5115075e12c848a9e4474cd47067c3200f7ff13c45f624f7383287e8e5e')

    depends_on('zstd')
    depends_on('boost')
    depends_on('protobuf')
    depends_on('pkgconfig')
    depends_on('openssl')
    depends_on('cmake @3.14:', type='build')
    depends_on('curl', type=('build', 'link'))

    root_cmakelists_dir = 'pulsar-client-cpp'

    def cmake_args(self):
        args = ["-DBUILD_PYTHON_WRAPPER=OFF", "-DBUILD_TESTS=OFF"]
        return args
