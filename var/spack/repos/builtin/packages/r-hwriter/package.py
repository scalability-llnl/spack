# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHwriter(RPackage):
    """HTML Writer - Outputs R objects in HTML format.

    Easy-to-use and versatile functions to
    output R objects in HTML format."""

    cran = "hwriter"

    license("LGPL-2.1-only")

    version("1.3.2.1", sha256="ed2fa254ab27cf65d397e181339976fc3261dfb4f6b600fea8c5689620dab6f3")
    version("1.3.2", sha256="6b3531d2e7a239be9d6e3a1aa3256b2745eb68aa0bdffd2076d36552d0d7322b")

    depends_on("r@2.6.0:", type=("build", "run"))
