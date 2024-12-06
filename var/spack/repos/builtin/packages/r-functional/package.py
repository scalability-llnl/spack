# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFunctional(RPackage):
    """Curry, Compose, and other higher-order functions

    Curry, Compose, and other higher-order functions"""

    cran = "functional"

    maintainers("jgaeb")

    license("GPL-2.0-or-later")

    version("0.6", sha256="19b78e27c27b1081245222c42da4dd1cb65c5643e6da9d6c1a6e997755c21888")
    version("0.4", sha256="05d1a50de6a574d938471c9a615c840871df9f879b2cbbcabc6b25b5809a70a8")
    version("0.2", sha256="1b11d039153a214e89e4903163522d8e15c1fcf84495023d9e463487bde1e8d8")
    version("0.1", sha256="148301d066f9c7e450d809a130d31b0763424f65f177704856d76143ded3db7e")
