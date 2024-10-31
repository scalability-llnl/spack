# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Doctest(CMakePackage):
    """The fastest feature-rich C++11/14/17/20/23 single-header testing framework"""

    homepage = "https://github.com/doctest/doctest"
    url = "https://github.com/doctest/doctest/archive/refs/tags/v2.4.11.tar.gz"

    license("MIT", checked_by="pranav-sivaraman")

    version("2.4.11", sha256="632ed2c05a7f53fa961381497bf8069093f0d6628c5f26286161fbd32a560186")

    depends_on("cxx", type="build")
    depends_on("cmake@3:", type="build")

    def cmake_args(self):
        args = [self.define("DOCTEST_WITH_TESTS", self.run_tests)]
        return args
