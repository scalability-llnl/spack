# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNpsurv(RPackage):
    """Nonparametric Survival Analysis.

    Non-parametric survival analysis of exact and interval-censored
    observations. The methods implemented are developed by Wang (2007)
    <doi:10.1111/j.1467-9868.2007.00583.x>, Wang (2008)
    <doi:10.1016/j.csda.2007.10.018>, Wang and Taylor (2013)
    <doi:10.1007/s11222-012-9341-9> and Wang and Fani (2018)
    <doi:10.1007/s11222-017-9724-z>."""

    cran = "npsurv"

    license("GPL-2.0-or-later")

    version("0.5-0", sha256="bc87db76e7017e178c2832a684fcd49c42e20054644b21b586413d26c8821dc6")
    version("0.4-0", sha256="404cf7135dc40a04e9b81224a543307057a8278e11109ba1fcaa28e87c6204f3")

    depends_on("r-lsei", type=("build", "run"))
