# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGraph(RPackage):
    """A package to handle graph data structures.

    A package that implements some simple graph handling capabilities."""

    bioc = "graph"

    version("1.78.0", commit="9df68e8f74e2b807b033f991d21142edfd1bc090")
    version("1.76.0", commit="e3efc108716e98bd3363621d17a6f9c3ef975d19")
    version("1.74.0", commit="4af608a5d9e1de33fda6ae28fb73bff9272ee296")
    version("1.72.0", commit="7afbd26ecd76e55e6bbd74915a561d7a9b15f907")
    version("1.68.0", commit="03ad9ed088095605e317510b8234501318994e94")
    version("1.62.0", commit="95223bd63ceb66cfe8d881f992a441de8b8c89a3")
    version("1.60.0", commit="e2aecb0a862f32091b16e0036f53367d3edf4c1d")
    version("1.58.2", commit="6455d8e7a5a45dc733915942cb71005c1016b6a0")
    version("1.56.0", commit="c4abe227dac525757679743e6fb4f49baa34acad")
    version("1.54.0", commit="2a8b08520096241620421078fc1098f4569c7301")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-biocgenerics@0.13.11:", type=("build", "run"))
