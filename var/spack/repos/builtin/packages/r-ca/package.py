# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------

from spack.package import *


class RCa(RPackage):
    """Simple, Multiple and Joint Correspondence Analysis.

    Computation and visualization of simple, multiple and joint correspondence
    analysis."""

    cran = "ca"

    license("GPL-2.0-or-later")

    version("0.71.1", sha256="040c2fc94c356075f116cc7cd880530b3c9e02206c0035182c03a525ee99b424")

    depends_on("r@3.0.0:", type=("build", "run"))
