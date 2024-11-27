# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Metal(CMakePackage):
    """METAL is a tool for the meta-analysis of genome-wide association studies"""

    homepage = "https://genome.sph.umich.edu/wiki/METAL"
    url = "https://github.com/statgen/METAL/archive/refs/tags/2020-05-05.tar.gz"

    license("BSD-3-Clause")

    version(
        "2020-05-05", sha256="0ffa2419ca2ab43766e7e6e8c97822c8ce1f5b6233fb5f992d1b1be1955fede7"
    )

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")
    depends_on("zlib-ng")

    @run_after("install")
    def mv_binary(self):
        with working_dir(self.build_directory):
            install_tree("bin", self.prefix.bin)
