# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nanopb(CMakePackage):
    """Nanopb is a small code-size Protocol Buffers implementation
    in ansi C."""

    homepage = "https://jpa.kapsi.fi/nanopb/"
    url = "https://github.com/nanopb/nanopb/archive/0.3.9.1.tar.gz"

    license("Zlib")

    version("0.3.9.1", sha256="b22d1f86d4adb2aa0436a277c4a59a5adfc467cafeb9bf405c27ef136599bbb3")

    depends_on("c", type="build")  # generated

    depends_on("protobuf", type=("build"))
    depends_on("py-protobuf", type=("build"))
