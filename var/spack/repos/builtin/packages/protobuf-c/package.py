# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ProtobufC(AutotoolsPackage):
    """
    Protocol Buffers implementation in C
    """

    homepage = "https://github.com/protobuf-c/protobuf-c"
    url = (
        "https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.2/protobuf-c-1.3.2.tar.gz"
    )
    maintainers("hyoklee")

    license("BSD-2-Clause")

    version("1.4.1", sha256="4cc4facd508172f3e0a4d3a8736225d472418aee35b4ad053384b137b220339f")
    version("1.3.2", sha256="53f251f14c597bdb087aecf0b63630f434d73f5a10fc1ac545073597535b9e74")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("protobuf@:3.21.12")
    depends_on("pkgconfig", type="build")
