# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioAdios2(CMakePackage):
    """An IO plugin to read/write ADIOS2 files for LibPressio"""

    homepage = "https://github.com/robertu94/libpressio_adios2"
    url = "https://github.com/robertu94/libpressio_adios2/archive/refs/tags/0.0.1.tar.gz"

    maintainers("robertu94")

    version("0.0.3", sha256="ca6a90dae1070f3ffe5c89b25966eb3142cb62820144e19ab4fd5b980531ba3b")
    version("0.0.2", sha256="8ab4b5a0dd8038d52f54aa9b5a67b83a8f7cd096db4c5a413fe0c6caf678e402")
    version("0.0.1", sha256="ab9c7e26114e8d81f8ad8aca703855079cd3441f9b72e01d9b4aeb0c57ce0746")

    depends_on("cxx", type="build")  # generated

    depends_on("libpressio@0.99.4:+mpi", when="@0.0.3:")
    depends_on("libpressio@0.85.0:+mpi", when="@0.0.2")
    depends_on("libpressio@0.60.0:+mpi")
    depends_on("adios2@2.8.0:+mpi")

    def cmake_args(self):
        args = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define("LIBPRESSIO_ADIOS2_WERROR", False),
        ]
        return args
