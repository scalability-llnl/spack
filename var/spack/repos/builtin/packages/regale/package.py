# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Regale(CMakePackage):
    """REGALE library is a C/C++ library developed in the European Project
    REGALE used to allow standard communication among HPC power stack tools."""

    homepage = "https://regale-project.eu/"
    url = "https://gricad-gitlab.univ-grenoble-alpes.fr/regale/tools/regale/-/archive/v1.0/regale-v1.0.tar.gz"

    license("Apache-2.0")

    version("1.0", sha256="894b0927372467e765049e79b855a9a277def65638013f68a1f2b6e837e35663")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("eprosima-fastdds")

    variant("examples", default=False, description="Build examples")
    variant("shared", default=True, description="Build shared libraries")

    def cmake_args(self):
        args = [
            self.define_from_variant("REGALE_EXAMPLES", "examples"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        return args
