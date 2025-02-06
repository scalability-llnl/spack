# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RCca(RPackage):
    """Canonical Correlation Analysis.

    Provides a set of functions that extend the 'cancor' function with new
    numerical and graphical outputs. It also include a regularized extension of
    the canonical correlation analysis to deal with datasets with more
    variables than observations."""

    cran = "CCA"

    version("1.2.2", sha256="f3b347f15dadd887f31206906e845c4893ec0cd7dc0c7e97c11001434c3d2e64")
    version("1.2.1", sha256="28febfce7c46039240346410e70f9d8795b536fc4e7e0d48d5370bd23cba9bd0")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-fields", type=("build", "run"))
    depends_on("r-fda", type=("build", "run"))
