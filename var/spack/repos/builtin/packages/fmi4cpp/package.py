# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fmi4cpp(CMakePackage):
    """FMI4cpp is a cross-platform FMI 2.0 implementation written in modern C++.
    FMI4cpp supports both Co-simulation and Model Exchange.
    """

    homepage = "https://github.com/NTNU-IHB/FMI4cpp"
    url = "https://github.com/NTNU-IHB/FMI4cpp/archive/refs/tags/v0.8.3.tar.gz"
    git = "https://github.com/NTNU-IHB/FMI4cpp.git"

    maintainers("prudhomm")
    license("MIT", checked_by="prudhomm")

    version("master", branch="master")
    version("0.8.3", sha256="f48c630f087bdf8d7a04611f6f30942c870c3c1211a94ef2404c40baa4bcb2c9")

    variant("shared", default=True, description="Build shared library")

    depends_on("cxx", type="build")
    depends_on("libzip")
    depends_on("pugixml")

    def cmake_args(self):
        args = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
        return args
