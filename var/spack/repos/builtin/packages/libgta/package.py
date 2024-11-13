# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libgta(CMakePackage):
    """Library that reads and writes Generic Tagged Arrays (GTA) files."""

    homepage = "https://marlam.de/gta/"
    url = "https://marlam.de/gta/releases/libgta-1.2.1.tar.xz"

    license("LGPL-2.1-or-later")

    version("1.2.1", sha256="d445667e145f755f0bc34ac89b63a6bfdce1eea943f87ee7a3f23dc0dcede8b1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.5:", type="build")

    def cmake_args(self):
        return [self.define("GTA_BUILD_DOCUMENTATION", False)]
