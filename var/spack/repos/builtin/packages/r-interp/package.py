# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RInterp(RPackage):
    """Interpolation Methods.

    Bivariate data interpolation on regular and irregular grids, either linear
    or using splines are the main part of this package. It is intended to
    provide FOSS replacement functions for the ACM licensed akima::interp and
    tripack::tri.mesh functions. Linear interpolation is implemented in
    interp::interp(..., method="linear"), this corresponds to the call
    akima::interp(..., linear=TRUE) which is the default setting and covers
    most of akima::interp use cases in depending packages. A re-implementation
    of Akimas irregular grid spline interpolation (akima::interp(...,
    linear=FALSE)) is now also available via interp::interp(...,
    method="akima"). Estimators for partial derivatives are now also available
    in interp::locpoly(), these are a prerequisite for the spline
    interpolation. The basic part is a GPLed triangulation algorithm (sweep
    hull algorithm by David Sinclair) providing the starting point for the
    irregular grid interpolator. As side effect this algorithm is also used to
    provide replacements for almost all functions of the tripack package which
    also suffers from the same ACM license restrictions. All functions are
    designed to be backward compatible with their akima / tripack
    counterparts."""

    cran = "interp"

    license("GPL-2.0-or-later")

    version("1.1-6", sha256="3674044e5334ecdf124054303929c084fc0797d3123e28576a230492ea6ecd34")
    version("1.1-4", sha256="4f7b5d388132a4d76e8635e2a7c4fa0d705df2b49e7d108faa16ce2236e34d06")
    version("1.1-3", sha256="b74e606b38cfb02985c1f9e3e45093620f76c0307b1b0b4058761e871eb5fa3f")

    depends_on("r@3.5.0:", type=("build", "run"))

    depends_on("r-rcpp@0.12.9:", type=("build", "run"))
    depends_on("r-deldir", type=("build", "run"))
    depends_on("r-rcppeigen", type=("build", "run"))
