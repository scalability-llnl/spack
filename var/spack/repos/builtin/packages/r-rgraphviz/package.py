# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgraphviz(RPackage):
    """Provides plotting capabilities for R graph objects.

    Interfaces R with the AT and T graphviz library for plotting R graph
    objects from the graph package."""

    bioc = "Rgraphviz"

    version("2.44.0", commit="1a1540d66afa0b5a693eee2acac8ad96cfc0a2e6")
    version("2.42.0", commit="f6877441ab256876ef6a62c2e6faf980c2190b20")
    version("2.40.0", commit="d864c9741c9177bc627cca1198673be2b1bfbc3e")
    version("2.38.0", commit="004de09a5b171211aff6cbaa1969ab8e3a5d6c61")
    version("2.34.0", commit="9746623211be794226258631992dfcccccfd7487")
    version("2.28.0", commit="c1f57c11f037c977f1d17f227f12a09a999e8c0b")
    version("2.26.0", commit="e9b08c77121a45c65129d94a12b5c0b31c65617f")
    version("2.24.0", commit="7d1fb00afed0d44e32b4a46f10137ab34f100577")
    version("2.22.0", commit="5b8ebbf9b38574c08959dd4632e802b3fbccc121")
    version("2.20.0", commit="eface6298150667bb22eac672f1a45e52fbf8c90")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r+X", type=("build", "run"))
    depends_on("r@2.6.0:", type=("build", "run"))
    depends_on("r-graph", type=("build", "run"))
    depends_on("graphviz@2.16:", type="run")
