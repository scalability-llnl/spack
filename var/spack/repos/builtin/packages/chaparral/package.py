# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chaparral(CMakePackage):
    """Radiation view factor library"""

    homepage = "https://gitlab.com/truchas/tpl-forks/chaparral"
    git = "https://gitlab.com/truchas/tpl-forks/chaparral.git"

    maintainers("pbrady", "zjibben")

    license("LGPL-2.1-or-later")

    version("develop", branch="truchas")
    version("2020-08-28", commit="c8a190bb74ef33ad8b2f7b67d20590f393fde32a", preferred=True)

    depends_on("c", type="build")  # generated

    variant("shared", default=True, description="Build shared library")
    variant("mpi", default=True, description="Build parallel library")

    depends_on("mpi", when="+mpi")
    depends_on("cmake@3.16:", type="build")

    def cmake_args(self):
        return [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("ENABLE_MPI", "mpi"),
        ]
