# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BppSeq(CMakePackage):
    """Bio++ seq library."""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/Installation"
    url = "https://github.com/BioPP/bpp-seq/archive/refs/tags/v2.4.1.tar.gz"

    maintainers("snehring")

    license("CECILL-2.0")

    version("2.4.1", sha256="dbfcb04803e4b7f08f9f159da8a947c91906c3ca8b20683ac193f6dc524d4655")
    version(
        "2.2.0",
        sha256="0927d7fb0301c1b99a7353d5876deadb4a3040776cc74e8fe1c366fe920e7b6b",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.6:", type="build")
    depends_on("bpp-core")

    def cmake_args(self):
        return ["-DBUILD_TESTING=FALSE"]
