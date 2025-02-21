# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RZcompositions(RPackage):
    """Treatment of Zeros, Left-Censored and Missing Values in Compositional
    Data Sets.

    Principled methods for the imputation of zeros, left-censored and missing
    data in compositional data sets (Palarea-Albaladejo and Martin-Fernandez
    (2015) <doi:10.1016/j.chemolab.2015.02.019>)."""

    cran = "zCompositions"

    version("1.5.0-4", sha256="73188e1e065a042723ed7a48df04e22317b204222d40744b83e8c392aae16aaf")
    version("1.4.0-1", sha256="33ee11f635cb87cc9c0617e1cfc91f1ac41c6cfe2b70fc441e226015939230e7")
    version("1.4.0", sha256="a00d7d0ba861988b1836e947fd521d58137a4def04a5d7aa73a099314b7e530c")
    version("1.3.4", sha256="ae22c86fe92368a26265933f42eecc518b9b69e7d9b698bc31bfaabfc3c48e95")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-nada", type=("build", "run"))
    depends_on("r-truncnorm", type=("build", "run"))
