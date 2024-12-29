# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Odc(CMakePackage):
    """ECMWF encoding and decoding of observational data in ODB2 format."""

    homepage = "https://github.com/ecmwf/odc"
    url = "https://github.com/ecmwf/odc/archive/refs/tags/1.3.0.tar.gz"

    maintainers("skosukhin", "climbfuji")

    license("Apache-2.0")

    version("1.5.2", sha256="49575c3ef9ae8825d588357022d0ff6caf3e557849888c9d2f0677e9efe95869")
    version("1.4.6", sha256="ff99d46175e6032ddd0bdaa3f6a5e2c4729d24b698ba0191a2a4aa418f48867c")
    version("1.4.5", sha256="8532d0453531d62e1f15791d1c5c96540b842913bd211a8ef090211eaf4cccae")
    version("1.3.0", sha256="97a4f10765b341cc8ccbbf203f5559cb1b838cbd945f48d4cecb1bc4305e6cd6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=False, description="Enable the Fortran interface")

    depends_on("ecbuild@3.4:", type="build")
    depends_on("cmake@3.12:", type="build")

    depends_on("eckit@1.4:+sql")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_FORTRAN", "fortran"),
            # The tests download additional data (~650MB):
            self.define("ENABLE_TESTS", self.run_tests),
        ]
        return args
