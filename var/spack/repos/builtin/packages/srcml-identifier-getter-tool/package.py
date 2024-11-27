# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SrcmlIdentifierGetterTool(CMakePackage):
    """SCANL's srcml_identifier_getter_tool. reads a srcML
    archive and outputs all identifiers in that archive through
    standard out."""

    homepage = "https://github.com/SCANL/srcml_identifier_getter_tool"
    git = "https://github.com/SCANL/srcml_identifier_getter_tool.git"

    version("2022-10-17", commit="01394c247ae6f61cc5864a9697e72e3623d8e7fb", submodules=True)

    depends_on("cxx", type="build")  # generated

    depends_on("libxml2")
    depends_on("zlib-api")
    depends_on("lzma")

    def install(self, spec, prefix):
        super().install(spec, prefix)
        mkdir(prefix.bin)
        install(join_path(self.build_directory, "bin", "grabidentifiers"), prefix.bin)
