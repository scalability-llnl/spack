# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQtl(RPackage):
    """Tools for Analyzing QTL Experiments.

    Analysis of experimental crosses to identify genes (called quantitative
    trait loci, QTLs) contributing to variation in quantitative traits. Broman
    et al. (2003) <doi:10.1093/bioinformatics/btg112>."""

    cran = "qtl"

    license("GPL-3.0-only")

    version("1.66", sha256="d46a7d49f2d0875c0c1cba77c993f995e7cac4db5796dfb1c62d9fa4eb60d681")
    version("1.60", sha256="8e9e5dfe2c6a76d4f69fb27add93ed0859ed3eaa23347310c2b9e3f07359d8ad")
    version("1.58", sha256="6eca5ac177ae62304d63c224f161b0f3ac9327ec1a03da5d7df2d5ddf4b09d97")
    version("1.52", sha256="320ac6172f2911ee772472becd68ff49a357c99fe7454335e4a19090d5788960")
    version("1.50", sha256="2d38656f04dc4187aefe56c29a8f915b8c7e222d76b84afe7045d272294f9ed5")
    version("1.47-9", sha256="6ba4e7b40d946b3ab68d54624599284b1d352c86fb50d31b134826be758ece41")
    version("1.44-9", sha256="315063f0c3fbb95cd2169eb4109ade0339e8f3c28670b38c3167214b9bdf950e")

    depends_on("r@2.14.0:", type=("build", "run"))
