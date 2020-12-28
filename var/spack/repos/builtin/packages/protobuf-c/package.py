# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ProtobufC(AutotoolsPackage):
    """
    Protocol Buffers implementation in C
    """

    homepage = "https://github.com/protobuf-c/protobuf-c"
    url      = "https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.2/protobuf-c-1.3.2.tar.gz"

    version('1.3.2', sha256='53f251f14c597bdb087aecf0b63630f434d73f5a10fc1ac545073597535b9e74')

    depends_on('protobuf')
    depends_on('pkgconfig', type='build')
