# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JhpcnDf(CMakePackage):
    """
    Data compression library based on Jointed Hierarchical Precision
    Compression Number - Data Format

    JHPCN-DF is a novel lossy compression algorithm taylored for floating
    point dataset. The algorithm enhances the effect of employing standard
    compression algorithms like deflate because this approach makes
    the occurence rate of the same byte pattern in data stream higher owing
    to truncating some lower bits of significand.
    """

    homepage = "https://avr-aics-riken.github.io/JHPCN-DF/"
    url = "https://github.com/avr-aics-riken/JHPCN-DF/archive/1.1.0.tar.gz"

    license("BSD-2-Clause")

    version("1.1.0", sha256="106d99cc4faac5c76e51e8bfe3193c1d3dc91648072cf418d868ed830592b04b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("lz4", default=False, description="Enable lz4")
    variant("fortran", default=False, description="Enable Fortran Interface")

    depends_on("zlib-api", type="link")
    depends_on("lz4@:1.7", when="+lz4", type="link")

    def cmake_args(self):
        args = [
            self.define_from_variant("with_Fortran_interface", "fortran"),
            self.define_from_variant("with_lz4", "lz4"),
        ]
        return args
