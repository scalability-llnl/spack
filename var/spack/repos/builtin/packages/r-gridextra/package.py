# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGridextra(RPackage):
    """Miscellaneous Functions for "Grid" Graphics.

    Provides a number of user-level functions to work with "grid" graphics,
    notably to arrange multiple grid-based plots on a page, and draw tables."""

    cran = "gridExtra"

    version("2.3", sha256="81b60ce6f237ec308555471ae0119158b115463df696d2eca9b177ded8988e3b")
    version("2.2.1", sha256="44fe455a5bcdf48a4ece7a542f83e7749cf251dc1df6ae7634470240398c6818")

    depends_on("r-gtable", type=("build", "run"))
