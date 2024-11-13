# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cli11(CMakePackage):
    """CLI11 is a command line parser for C++11 and beyond that provides a rich
    feature set with a simple and intuitive interface."""

    homepage = "https://cliutils.github.io/CLI11/book/"
    url = "https://github.com/CLIUtils/CLI11/archive/v1.9.1.tar.gz"
    maintainers("nightlark")

    license("BSD-3-Clause")

    version("2.4.2", sha256="f2d893a65c3b1324c50d4e682c0cdc021dd0477ae2c048544f39eed6654b699a")
    version("2.4.1", sha256="73b7ec52261ce8fe980a29df6b4ceb66243bb0b779451dbd3d014cfec9fdbb58")
    version("2.3.2", sha256="aac0ab42108131ac5d3344a9db0fdf25c4db652296641955720a4fbe52334e22")
    version("2.3.1", sha256="378da73d2d1d9a7b82ad6ed2b5bda3e7bc7093c4034a1d680a2e009eb067e7b2")
    version("2.1.1", sha256="d69023d1d0ab6a22be86b4f59d449422bc5efd9121868f4e284d6042e52f682e")
    version("2.1.0", sha256="2661b0112b02478bad3dc7f1749c4825bfc7e37b440cbb4c8c0e2ffaa3999112")
    version("2.0.0", sha256="2c672f17bf56e8e6223a3bfb74055a946fa7b1ff376510371902adb9cb0ab6a3")
    version("1.9.1", sha256="c780cf8cf3ba5ec2648a7eeb20a47e274493258f38a9b417628e0576f473a50b")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.4:", type="build")
    depends_on("cmake@3.5:", type="build", when="@2.4:")

    def cmake_args(self):
        args = [
            self.define("CLI11_BUILD_EXAMPLES", False),
            self.define("CLI11_BUILD_DOCS", False),
            self.define("CLI11_BUILD_TESTS", False),
            self.define("CLI11_PRECOMPILED", True),
        ]
        return args
