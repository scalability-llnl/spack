# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastor(CMakePackage):
    """Fastor is a lightweight high performance tensor algebra framework
    for modern C++."""

    homepage = "https://github.com/romeric/Fastor"
    url = "https://github.com/romeric/Fastor/archive/refs/tags/V0.6.4.tar.gz"
    git = "https://github.com/romeric/Fastor.git"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("0.6.4", sha256="c97a3b9dbb92413be90689af9d942cddee12a74733cf42f1a8014965553a11f8")

    depends_on("cxx", type="build")

    depends_on("cmake@3.20:", type="build")

    def cmake_args(self):
        return [self.define("BUILD_TESTING", self.run_tests)]
