# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffycontam(RPackage):
    """structured corruption of affymetrix cel file data.

    structured corruption of cel file data to demonstrate QA
    effectiveness"""

    bioc = "affyContam"

    version("1.58.0", commit="5e91d79d7653a4f484b62eae7fd7e908de8cb9b6")
    version("1.56.0", commit="e2b8a4fba1648255eadce954a848f2dd8e22bcb3")
    version("1.54.0", commit="c5208b48b8881983ff53a4713244327e8ad13b78")
    version("1.52.0", commit="47c1d86da330f157d3ece0e26b0657d66a5ca0c9")
    version("1.48.0", commit="88387a2ad4be4234d36710c65f2ca3a5b06b67da")
    version("1.42.0", commit="8a5e94a5ae8c2ecfafa6177b84a6e8ab07e14fbe")
    version("1.40.0", commit="dfd5fd6ae04941dddbda03f656540b71b2fbc614")
    version("1.38.0", commit="84651e8eade61619afefc83bb290047da101a5bc")
    version("1.36.0", commit="aeb684a7d3f6fa9243f3946d214de53649fa4fd6")
    version("1.34.0", commit="03529f26d059c19e069cdda358dbf7789b6d4c40")

    depends_on("r@2.7.0:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-affy", type=("build", "run"))
    depends_on("r-affydata", type=("build", "run"))
