# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSplines2(RPackage):
    """Constructs basis functions of B-splines, M-splines, I-splines, convex
    splines (C-splines), periodic splines, natural cubic splines, generalized
    Bernstein polynomials, their derivatives, and integrals (except C-splines)
    by closed-form recursive formulas. It also contains a C++ head-only library
    integrated with Rcpp. See Wang and Yan (2021) <doi:10.6339/21-JDS1020>
    for details."""

    homepage = "https://wwenjie.org/splines2"
    cran = "splines2"

    license("GPL-3.0-or-later", checked_by="wdconinc")

    version("0.5.3", sha256="c27e7bd12d615095f765f4c1ed3cb9e39b922653aabbe88c4ca3ac31e6a01ddc")

    depends_on("r@3.2.3:", type=("build", "run"))

    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))
