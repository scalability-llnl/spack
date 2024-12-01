# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SraTools(CMakePackage):
    """The SRA Toolkit and SDK from NCBI is a collection of tools and
    libraries for using data in the INSDC Sequence Read Archives."""

    homepage = "https://github.com/ncbi/sra-tools"
    git = "https://github.com/ncbi/sra-tools.git"

    version("3.0.3", tag="3.0.3", commit="01f0aa21bb20b84c68ea34404d43da680811e27a")
    version("3.0.0", tag="3.0.0", commit="bd2053a1049e64207e75f4395fd1be7f1572a5aa")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("openjdk")
    depends_on("flex@2.6:")
    depends_on("libxml2")
    depends_on("ncbi-vdb")
    depends_on("ncbi-vdb@3.0.2:", when="@3.0.3:")

    # The CMakeLists.txt  file set the path to ${TARGDIR}/obj but the code
    # actually uses ${TARGDIR}.
    patch("ngs-java.patch")

    def cmake_args(self):
        args = [
            self.define("VDB_INCDIR", format(self.spec["ncbi-vdb"].prefix) + "/include"),
            self.define("VDB_LIBDIR", format(self.spec["ncbi-vdb"].prefix) + "/lib64"),
            self.define("VDB_BINDIR", format(self.spec["ncbi-vdb"].prefix)),
        ]
        return args
