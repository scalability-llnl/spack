# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAmap(RPackage):
    """Another Multidimensional Analysis Package.

    Tools for Clustering and Principal Component Analysis (With robust methods,
    and parallelized functions)."""

    cran = "amap"

    license("GPL-2.0-or-later")

    version("0.8-19", sha256="7349ea684b69eba0fcc48f78b7ac09a838d95d3bc0c6a94b6055605ac0291900")
    version("0.8-18", sha256="7afbbdd681a201121374821b733c9000ca1046a2353ee386507604c2c759ec7e")
    version("0.8-17", sha256="6b8473d1d35a9cbc611661882c8f681162e8f913f911ccd51629200ae72289c6")
    version("0.8-16", sha256="d3775ad7f660581f7d2f070e426be95ae0d6743622943e6f5491988e5217d4e2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@0.8-17:")
