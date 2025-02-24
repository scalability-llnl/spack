# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCardata(RPackage):
    """Companion to Applied Regression Data Sets.

    Datasets to Accompany J. Fox and S. Weisberg, An R Companion to Applied
    Regression, Third Edition, Sage (2019)."""

    cran = "carData"

    version("3.0-5", sha256="02e77159b33e3afb8cd9cfab11cf5a996a93175f924b07d991ce44bc6e16451a")
    version("3.0-4", sha256="cda6f5e3efc1d955a4a0625e9c33f90d49f5455840e88b3bd757129b86044724")
    version("3.0-2", sha256="3b5c4eff1cc1e456a5331084774503eaa06cf61fb7acf6b9e8a6bfabd5735494")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.0-4:")
