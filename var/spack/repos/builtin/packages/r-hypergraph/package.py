# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHypergraph(RPackage):
    """A package providing hypergraph data structures.

    A package that implements some simple capabilities for representing and
    manipulating hypergraphs."""

    bioc = "hypergraph"

    version("1.72.0", commit="1b619b8dfeaf13dca7857013495d52dcfe4276b4")
    version("1.70.0", commit="a5ffeafa8b999b5e7e77f93f4e6284abafc81621")
    version("1.68.0", commit="7d53b5050f4ebe0a7007c02b76e93498195da3a4")
    version("1.66.0", commit="e9c47336df6409006622818f541f258103163a39")
    version("1.62.0", commit="a286bbb70289e9f3cdf41407d52e5976bd6ed11e")
    version("1.56.0", commit="f8b977fe068f15ecea49d30e77a871a35afcb97b")
    version("1.54.0", commit="cf134b9221e9b5f6329a6786a366f57426c49e7c")
    version("1.52.0", commit="3e28d8e8ab4c3facb79857b4e4cfffd65e064aca")
    version("1.50.0", commit="fb3d523caf1d5791ef6962dd3c1a142742025ad5")
    version("1.48.0", commit="a4c19ea0b5f15204f706a7bfdea5363706382820")

    depends_on("r@2.1.0:", type=("build", "run"))
    depends_on("r-graph", type=("build", "run"))
