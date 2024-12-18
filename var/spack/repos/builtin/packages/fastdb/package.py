# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastdb(MakefilePackage):
    """Object-Relational Main-Memory Embedded Database system
    tightly integrated with C++ language."""

    homepage = "https://sourceforge.net/projects/fastdb/"
    url = "https://sourceforge.net/projects/fastdb/files/fastdb/3.75/fastdb-3.75.tar.gz"

    version("3.75", sha256="eeafdb2ad01664c29e2d4053a305493bdedc8e91612ab25f1d36ad2f95b0dad6")
    version("3.74", sha256="4d0c9a165a1031860d4853d7084b8fe4627f0004861e6070927d3b6c594af889")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("fastdb-fmax-fmin.patch")

    def install(self, spec, prefix):
        make("PREFIX=%s" % prefix, "install")
