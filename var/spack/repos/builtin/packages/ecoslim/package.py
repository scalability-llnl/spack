# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ecoslim(CMakePackage):
    """EcoSLIM is a Lagrangian, particle-tracking code that simulates
    advective and diffusive movement of water parcels.  EcoSLIM
    integrates seamlessly with ParFlow-CLM."""

    homepage = "https://github.com/reedmaxwell/EcoSLIM"
    url = "https://github.com/reedmaxwell/EcoSLIM/archive/refs/tags/v1.3.tar.gz"
    git = "https://github.com/reedmaxwell/EcoSLIM.git"

    maintainers("reedmaxwell", "lecondon", "smithsg84")

    license("LGPL-3.0-or-later")

    version("1.3", sha256="b532e570b4767e4fa84123d8773732150679e8e3d7fecd5c6e99fb1d4dc57b84")
    version("master", branch="master")

    depends_on("fortran", type="build")  # generated

    def cmake_args(self):
        """Populate cmake arguments for EcoSLIM."""
        return []
