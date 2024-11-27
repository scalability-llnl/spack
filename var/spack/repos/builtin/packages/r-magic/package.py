# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMagic(RPackage):
    """Create and Investigate Magic Squares.

    A collection of efficient, vectorized algorithms for the creation and
    investigation of magic squares and hypercubes, including a variety of
    functions for the manipulation and analysis of arbitrarily dimensioned
    arrays. The package includes methods for creating normal magic squares of
    any order greater than 2. The ultimate intention is for the package to be a
    computerized embodiment all magic square knowledge, including direct
    numerical verification of properties of magic squares (such as recent
    results on the determinant of odd-ordered semimagic squares). Some
    antimagic functionality is included. The package also serves as a rebuttal
    to the often-heard comment "I thought R was just for statistics"."""

    cran = "magic"

    license("GPL-2.0-only")

    version("1.6-1", sha256="ca79ec7ae92b736cb128556c081abf547f49956c326e053a76579889cbcb7976")
    version("1.6-0", sha256="4516d48c9618e3f395db873e886f5deb3b66b32ebe10d4c26c1420ac848acbbf")
    version("1.5-9", sha256="fa1d5ef2d39e880f262d31b77006a2a7e76ea38e306aae4356e682b90d6cd56a")
    version("1.5-8", sha256="7f8bc26e05003168e9d2dadf64eb9a34b51bc41beba482208874803dee7d6c20")
    version("1.5-6", sha256="1b6c3f5bef0ddc28c4b68894051df5d9c0d4985d9e6ad81892369d0f7fe0298d")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
