# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNumderiv(RPackage):
    """Accurate Numerical Derivatives.

    Methods for calculating (usually) accurate numerical first and second order
    derivatives. Accurate calculations are done using 'Richardson"s'
    extrapolation or, when applicable, a complex step derivative is available.
    A simple difference method is also provided. Simple difference is (usually)
    less accurate but is much quicker than 'Richardson"s' extrapolation and
    provides a useful cross-check. Methods are provided for real scalar and
    vector valued functions."""

    cran = "numDeriv"

    version(
        "2016.8-1.1", sha256="d8c4d19ff9aeb31b0c628bd4a16378e51c1c9a3813b525469a31fe89af00b345"
    )
    version("2016.8-1", sha256="1b681d273697dc780a3ac5bedabb4a257785732d9ca4ef68e4e4aac8b328d11e")

    depends_on("r@2.11.1:", type=("build", "run"))
