# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXde(RPackage):
    """a Bayesian hierarchical model for cross-study analysis of
       differential gene expression.

    Multi-level model for cross-study detection of differential gene
    expression."""

    bioc = "XDE"

    version("2.46.0", commit="f94324fba1ad6dca129d86e61abc219f766321e8")
    version("2.44.0", commit="a6ddedb91afe381f223e52ae49c6704f8f046916")
    version("2.42.0", commit="298e83eff7fc5f72a2bb76b559c5115c6cd3ee84")
    version("2.40.0", commit="bfc3c54787aec97b70bef7b99a6adc75d2cf5ed2")
    version("2.36.0", commit="0277f9dffbd7d1880be77cb8581fc614501b3293")
    version("2.30.0", commit="058af6f1e431522778f970bf61f834620d3d7dd7")
    version("2.28.0", commit="b8cc7d0840ce1324644e8b4a750fbb964884498b")
    version("2.26.0", commit="7bf6368037937c53542447175061c2e2059ee3be")
    version("2.24.0", commit="fd5f245f82893657dc36e5a67a1d3b8255772462")
    version("2.22.0", commit="25bcec965ae42a410dd285a9db9be46d112d8e81")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-biobase@2.5.5:", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-genefilter", type=("build", "run"))
    depends_on("r-gtools", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"), when="@2.24.0:")
    depends_on("r-genemeta", type=("build", "run"), when="@2.24.0:")
    depends_on("r-siggenes", type=("build", "run"), when="@2.24.0:")

    depends_on("r-mergemaid", type=("build", "run"), when="@:2.30.0")
