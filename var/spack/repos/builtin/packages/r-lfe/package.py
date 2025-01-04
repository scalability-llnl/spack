# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLfe(RPackage):
    """Linear Group Fixed Effects.

    Transforms away factors with many levels prior to doing an OLS. Useful for
    estimating linear models with multiple group fixed effects, and for
    estimating linear models which uses factors with many levels as pure
    control variables. See Gaure (2013) <doi:10.1016/j.csda.2013.03.024>
    Includes support for instrumental variables, conditional F statistics for
    weak instruments, robust and multi-way clustered standard errors, as well
    as limited mobility bias correction (Gaure 2014 <doi:10.1002/sta4.68>).
    WARNING: This package is NOT under active development anymore, no further
    improvements are to be expected, and the package is at risk of being
    removed from CRAN."""

    cran = "lfe"

    license("Artistic-2.0")

    version("3.0-0", sha256="342d05c32932d0db755c35a7e27da1001a38e375866c6f61a18259faf0430399")
    version("2.9-0", sha256="7c9a9cd74ad98c65b67477eb6924409d7e372d01d7ed50fa2edb6fa34e02223c")
    version("2.8-8", sha256="0fc22928fa16f22ee66c8e426a0e994346ad2f67b3c5aea597f3eeffbd85ab71")
    version("2.8-7.1", sha256="d6a1efd8c43f84fa291e4959938f16e85bf5feef113515aaca1fe90075a78c50")
    version("2.8-6", sha256="bf5fd362e9722e871a5236f30da562c489ae6506b667609b9465eefa8f101612")
    version("2.8-5", sha256="fd80c573d334594db933ff38f67bd4c9f899aaf648c3bd68f19477a0059723c2")
    version("2.8-4", sha256="ee5f6e312214aa73e285ae84a6bdf49ba10e830f1a68ffded2fea2e532f2cd6a")

    depends_on("r@2.15.2:", type=("build", "run"))
    depends_on("r-matrix@1.1-2:", type=("build", "run"))
    depends_on("r-formula", type=("build", "run"))
    depends_on("r-xtable", type=("build", "run"))
    depends_on("r-sandwich", type=("build", "run"))
