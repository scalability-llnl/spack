# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffycomp(RPackage):
    """Graphics Toolbox for Assessment of Affymetrix Expression Measures.

    The package contains functions that can be used to compare expression
    measures for Affymetrix Oligonucleotide Arrays."""

    bioc = "affycomp"

    version("1.76.0", commit="8bfc628de26a739c5e0cb47aa22bfda7c8d0a922")
    version("1.74.0", commit="1160d6395f23085456938ba2bd38fb45597fc92f")
    version("1.72.0", commit="c52baea98b80abd4a99380ac9d4b68ef91869d40")
    version("1.70.0", commit="487f6775975092475581a6c02ddb27590559cf07")
    version("1.66.0", commit="388d01af8b1e6ab11051407f77d0206512df8424")
    version("1.60.0", commit="5dbe61fa04941529a0fc70b728021c8e00c4ba0c")
    version("1.58.0", commit="99607b2c4aad37e3e63eccbd12d0d533762f28ef")
    version("1.56.0", commit="b0994da338be19396e647c680059fd35341b50a2")
    version("1.54.0", commit="65281c1ca37147c2a54ad3722a8d5ff0ffa5acc5")
    version("1.52.0", commit="1b97a1cb21ec93bf1e5c88d5d55b988059612790")

    depends_on("r@2.13.0:", type=("build", "run"))
    depends_on("r-biobase@2.3.3:", type=("build", "run"))
