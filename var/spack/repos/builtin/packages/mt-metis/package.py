# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MtMetis(CMakePackage):
    """
    mt-Metis is a multithreaded multilevel graph partitioning an ordering
    tool. It is based on the algorithms used in Metis and ParMetis
    """

    homepage = "http://glaros.dtc.umn.edu/gkhome/views/metis"
    url = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/mt-metis-0.6.0.tar.gz"

    license("MIT")

    version("0.6.0", sha256="cb8fb836b630a899edbeca4e1da19ec9eb47e89903bda83e7ec62cb0ffdcc284")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # avoid asm('pause') for no x86_64 familly.
    patch("non_x8664.patch")

    variant("shared", default=True, description="Enable build of shared libraries")

    def cmake_args(self):
        cmake_args = [
            self.define("DOMLIB_PATH", "domlib"),
            self.define("WILDRIVER_PATH", "wildriver"),
            self.define("METIS_PATH", "metis"),
            self.define_from_variant("SHARED", "shared"),
        ]
        return cmake_args

    @property
    def libs(self):
        return find_libraries(["libmtmetis", "libwildriver"], self.prefix.lib)
