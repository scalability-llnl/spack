# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmutil(RPackage):
    """Utilities for Nonlinear Regression and Repeated MeasurementsModels.

    A toolkit of functions for nonlinear regression and repeated measurements
    not to be used by itself but called by other Lindsey packages such as
    'gnlm', 'stable', 'growth', 'repeated', and 'event'  (available at
    <https://www.commanster.eu/rcode.html>)."""

    cran = "rmutil"

    license("GPL-2.0-or-later")

    version("1.1.10", sha256="819fd7ce695cc742b4594705986eb06764460fc88521ea32de793c49de7ca5f9")
    version("1.1.9", sha256="3a68cc4058394fcb6bab960a680bad939ad7270888f4c271ca6438e49670333c")
    version("1.1.5", sha256="6077e643d6daeba6edcf49d928320b54cc6aa6ff59934f9e9e6071a2f9afb2f6")
    version("1.1.3", sha256="7abaf41e99d1c4a0e4082c4594964ac1421c53b4268116c82fa55aa8bc0582da")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r@1.4:", type=("build", "run"))
