# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGsl(RPackage):
    """Wrapper for the Gnu Scientific Library.

    An R wrapper for some of the functionality of the Gnu Scientific
    Library."""

    cran = "gsl"

    license("GPL-3.0-only")

    version("2.1-8", sha256="f33609bf485abd190e65ff5d0fdab438b759294c47b921d983d89d6f053a2d95")
    version("2.1-7.1", sha256="ee98d1382d37ffa77538a90ccdbf44affbf1710a9e66b8ada73fa72e67921985")
    version("2.1-6", sha256="f5d463239693f146617018987687db31b163653708cbae0b730b9b7bed81995c")

    depends_on("c", type="build")  # generated

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@2.1-8:")
    depends_on("gsl@2.1:")
