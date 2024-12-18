# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HbmDramsim2(MakefilePackage):
    """
    HBM Simulator based on DRAMSim2
    """

    homepage = "https://github.com/tactcomplabs/HBM"
    git = "https://github.com/tactcomplabs/HBM"
    url = "https://github.com/tactcomplabs/HBM/archive/hbm-1.0.0-release.tar.gz"

    maintainers("jjwilke")

    version("1.0.0", sha256="0efad11c58197edb47ad1359f8f93fb45d882c6bebcf9f2143e0df7a719689a0")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        install_tree(".", prefix)
