# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStrucchangercpp(RPackage):
    """Testing, Monitoring, and Dating Structural Changes: C++ Version.

    A fast implementation with additional experimental features for testing,
    monitoring and dating structural changes in (linear) regression models.
    'strucchangeRcpp' features tests/methods from the generalized fluctuation test
    framework as well as from the F test (Chow test) framework. This includes
    methods to fit, plot and test fluctuation processes (e.g. cumulative/moving
    sum, recursive/moving estimates) and F statistics, respectively. These methods
    are described in Zeileis et al. (2002) <doi:10.18637/jss.v007.i02>. Finally,
    the breakpoints in regression models with structural changes can be estimated
    together with confidence intervals, and their magnitude as well as the model
    fit can be evaluated using a variety of statistical measures."""

    cran = "strucchangeRcpp"

    version(
        "1.5-3-1.0.4", sha256="f506fcb593ce4bacf1892de25154257d0fe02260ef956a75438c6330195cd86d"
    )

    depends_on("cxx", type="build")  # generated

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-zoo", type=("build", "run"))
    depends_on("r-sandwich", type=("build", "run"))
    depends_on("r-rcpp@0.12.7:", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))
