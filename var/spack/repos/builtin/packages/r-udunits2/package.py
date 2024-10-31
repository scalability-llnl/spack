# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUdunits2(RPackage):
    """Udunits-2 Bindings for R.

    Provides simple bindings to Unidata's udunits library."""

    cran = "udunits2"

    license("GPL-2.0-only")

    version("0.13.2.1", sha256="9f5429c04a24930f7d037d506e5b154b6154df69247dcdaa6261075291d7f902")
    version("0.13.2", sha256="ee00898801b3282717cba40a9ef930515506386aa82a050356d1a9c80a9f5969")
    version("0.13", sha256="d155d3c07f6202b65dec4075ffd1e1c3f4f35f5fdece8cfb319d39256a3e5b79")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("udunits")
