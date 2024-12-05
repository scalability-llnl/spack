# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lcgenv(Package):
    """This package provides environment for packages in SFT LCG releases."""

    homepage = "https://gitlab.cern.ch/GENSER/lcgenv"
    url = "https://gitlab.cern.ch/GENSER/lcgenv/-/archive/v1.3.19/lcgenv-v1.3.19.tar.gz"

    maintainers("haralmha")

    license("MIT")

    version("1.3.19", sha256="b091743705cf84ff5de60487f2f73cbf9d10676577cd1d99bbde00d3616d0751")

    def install(self, spec, prefix):
        install_tree(".", prefix)
