# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Thermo4pfm(CMakePackage):
    """Library to evaluate alloy compositions in Phase-Field models"""

    homepage = "https://github.com/ORNL/Thermo4PFM"
    url = "https://github.com/ORNL/Thermo4PFM/archive/refs/tags/v1.1.1.tar.gz"

    maintainers("jeanlucf22")

    license("BSD-3-Clause")

    version("1.1.1", sha256="cff3c83405224a39bb34c57e444e208e94c6782d84303acd0588d1dfa61513a1")

    depends_on("cxx", type="build")  # generated

    depends_on("boost")
