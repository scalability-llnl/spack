# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Multicharge(CMakePackage):
    """Electronegativity equilibration model for atomic partial charges"""

    homepage = "https://github.com/grimme-lab/multicharge"
    url = "https://github.com/grimme-lab/multicharge/releases/download/v0.0.0/multicharge-0.0.0.tar.xz"
    git = "https://github.com/grimme-lab/multicharge.git"

    maintainers("RMeli", "awvwgk")

    license("Apache-2.0", checked_by="RMeli")

    version("0.3.0", md5="7586576a425e4f3c74e5644049d100d7")

    variant("openmp", default=True, description="Enable OpenMP support")

    depends_on("lapack")
    depends_on("mctc-lib")

    def cmake_args(self):
        args = [
            self.define_from_variant("WITH_OpenMP", "openmp"),
        ]
        return args
