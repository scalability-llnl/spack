# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Elfio(CMakePackage):
    """
    ELFIO is a header-only C++ library intended for reading and generating
    files in the ELF binary format.
    """

    homepage = "https://github.com/serge1/ELFIO"
    url = "https://github.com/serge1/ELFIO/releases/download/Release_3.9/elfio-3.9.tar.gz"

    maintainers("haampie")

    license("MIT")

    version("3.11", sha256="3307b104c205399786edbba203906de9517e36297709fe747faf9478d55fbb91")
    version("3.10", sha256="cdc6362ede2e0c8d1d6db15d7da4b526f461d9cfae6f6337369e416a8bc60234")
    version("3.9", sha256="767b269063fc35aba6d361139f830aa91c45dc6b77942f082666876c1aa0be0f")
    version("3.8", sha256="9553ce2b8d8aa2fb43f0e9be9bcbd10cd52f40b385110ea54173889c982f9ac4")
    version("3.7", sha256="0af2452214c32639f8dbe520b31e03802be184581ab5ad65e99ed745274dbd5d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # note, 3.10 is required on master it seems
    depends_on("cmake@3.12:", when="@3.8:", type="build")
    depends_on("cmake@3.12.4:", when="@3.7", type="build")

    def cmake_args(self):
        return [
            self.define("ELFIO_BUILD_EXAMPLES", "OFF"),
            self.define("ELFIO_BUILD_TESTS", "OFF"),
        ]
