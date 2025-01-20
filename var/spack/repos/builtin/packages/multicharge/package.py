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

    version("0.3.0", sha256="e8f6615d445264798b12d2854e25c93938373dc149bb79e6eddd23fc4309749d")

    variant("openmp", default=True, description="Enable OpenMP support")

    depends_on("lapack")
    depends_on("mctc-lib")

    def cmake_args(self):
        args = [self.define_from_variant("WITH_OpenMP", "openmp")]
        return args
