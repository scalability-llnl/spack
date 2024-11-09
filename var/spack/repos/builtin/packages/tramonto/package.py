# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tramonto(CMakePackage):
    """Tramonto: Software for Nanostructured Fluids in Materials and Biology"""

    homepage = "https://software.sandia.gov/tramonto/"
    git = "https://github.com/Tramonto/Tramonto.git"

    version("develop", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("trilinos@:12+nox")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.extend(["-DTRILINOS_PATH:PATH=%s/lib/cmake/Trilinos" % spec["trilinos"].prefix])
        return args
