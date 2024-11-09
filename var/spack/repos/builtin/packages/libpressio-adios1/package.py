# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class LibpressioAdios1(CMakePackage):
    """LibPressio file reader for legacy ADIOS1 files not supported by ADIOS2"""

    homepage = "https://github.com/robertu94/libpressio-adios1"
    url = "https://github.com/robertu94/libpressio-adios1/archive/refs/tags/0.0.1.tar.gz"
    git = "https://github.com/robertu94/libpressio-adios1"

    maintainers("robertu94")

    version("0.0.2", sha256="cb3c4ef3c9c3bd5f4c08d1145a07d2ce0c84605a2213b744992c6c8cef998d39")

    depends_on("cxx", type="build")  # generated

    depends_on("adios")
    depends_on("libpressio")

    def cmake_args(self):
        args = ["-DCMAKE_MODULE_PATH={}".format(self.spec["adios"].prefix.etc)]
        return args
