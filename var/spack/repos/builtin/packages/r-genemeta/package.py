# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenemeta(RPackage):
    """MetaAnalysis for High Throughput Experiments.

    A collection of meta-analysis tools for analysing high throughput
    experimental data"""

    bioc = "GeneMeta"

    version("1.78.0", commit="4d17ec8babebad5b49b007d2791181f95cb39a02")
    version("1.76.0", commit="2eed8386ee1a40e4ab14594323e4538b7f73f8e9")
    version("1.74.0", commit="476eb5edef69cc05d4178faaf02ef45293c91f32")
    version("1.72.0", commit="1cb047172f54c12c5dc5a9b39358ea04cbeff8a2")
    version("1.70.0", commit="e5db82e04efc4572358abce7e0c09273f94c9d72")
    version("1.68.0", commit="4213c0205d477660195300a0aa9751972f86bf91")
    version("1.66.0", commit="c16eb09492f08f6cc0f253fafa3fa5dce35dcdba")
    version("1.62.0", commit="eb4273ff5867e39592f50b97b454fa5e32b4a9bf")
    version("1.56.0", commit="cb2c9e353d34ea9f3db06cb236c7a89674f2682d")
    version("1.54.0", commit="932553cd8df82b7df804fccda9bfd4b0f36d79d7")
    version("1.52.0", commit="1f21759984a5852c42a19e89ee53ffd72053d49c")
    version("1.50.0", commit="0f8603653285698ed451fcbf536a4b3f90015f92")
    version("1.48.0", commit="68c65304d37f5a4722cf4c25afb23214c3a2f4c8")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-biobase@2.5.5:", type=("build", "run"))
    depends_on("r-genefilter", type=("build", "run"))
