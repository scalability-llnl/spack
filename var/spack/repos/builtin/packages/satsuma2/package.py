# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Satsuma2(CMakePackage):
    """Satsuma2 is an optimsed version of Satsuma, a tool to reliably align
    large and complex DNA sequences providing maximum sensitivity (to find
    all there is to find), specificity (to only find real homology) and
    speed (to accomodate the billions of base pairs in vertebrate genomes).
    """

    homepage = "https://github.com/bioinfologics/satsuma2"
    git = "https://github.com/bioinfologics/satsuma2.git"

    version("2021-03-04", commit="37c5f386819614cd3ce96016b423ddc4df1d86ec")
    version("2016-11-22", commit="da694aeecf352e344b790bea4a7aaa529f5b69e6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    maintainers("snehring")

    def patch(self):
        filter_file(
            "(^#include <unistd.h>$)", "\\1\n#include <memory>", "analysis/SatsumaSynteny2.cc"
        )

    def install(self, spec, prefix):
        install_tree(join_path(self.build_directory, "bin"), prefix.bin)
