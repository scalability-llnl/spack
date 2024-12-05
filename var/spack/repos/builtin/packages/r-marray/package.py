# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMarray(RPackage):
    """Exploratory analysis for two-color spotted microarray data.

    Class definitions for two-color spotted microarray data. Fuctions for data
    input, diagnostic plots, normalization and quality checking."""

    bioc = "marray"

    license("GPL-2.0-or-later")

    version("1.78.0", commit="97d74b2af40568eda445378b4708a2e2d33291cd")
    version("1.76.0", commit="88cb0fd21cc60ac65410ca4314eca2e351933ec5")
    version("1.74.0", commit="9130a936fffb7d2d445ff21d04520e78b62625ac")
    version("1.72.0", commit="da35e8b8d2c9ef17e779013a5d252f38a1c66633")
    version("1.68.0", commit="67b3080486abdba7dd19fccd7fb731b0e8b5b3f9")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
