# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhytools(RPackage):
    """Phylogenetic Tools for Comparative Biology (and Other Things).

    A wide range of functions for phylogenetic analysis. Functionality is
    concentrated in phylogenetic comparative biology, but also includes
    numerous methods for visualizing, manipulating, reading or writing, and
    even inferring phylogenetic trees and data. Included among the functions in
    phylogenetic comparative biology are various for ancestral state
    reconstruction, model-fitting, simulation of phylogenies and data, and
    multivariate analysis. There are a broad range of plotting methods for
    phylogenies and comparative data which include, but are not restricted to,
    methods for mapping trait evolution on trees, for projecting trees into
    phenotypic space or a geographic map, and for visualizing correlated
    speciation between trees. Finally, there are a number of functions for
    reading, writing, analyzing, inferring, simulating, and manipulating
    phylogenetic trees and comparative data not covered by other packages. For
    instance, there are functions for randomly or non-randomly attaching
    species or clades to a phylogeny, for estimating supertrees or consensus
    phylogenies from a set, for simulating trees and phylogenetic data under a
    range of models, and for a wide variety of other manipulations and analyses
    that phylogenetic biologists might find useful in their research."""

    cran = "phytools"

    license("GPL-2.0-or-later")

    version("2.3-0", sha256="973020a695be3fef94a37d7d6732d9352b66e44d30feb554d267b6aeb646d081")
    version("1.5-1", sha256="f8be59abbff1f5032be4523c361da53b0d5b71677fedebba6d7cbae2dca7e101")
    version("1.2-0", sha256="ba3c684118c0eaab4601b21988c553ce7ee019df1714d2ac8d4451075f843b86")
    version("1.0-3", sha256="bfe2aec6aae8235264c1494eee42be494fed81a676c6de9e39c57a6e3682b37d")
    version("1.0-1", sha256="b7bf5d35ec4205115112481f6761de3e276e6b086a3e5249621ad63aa23a1ac8")
    version("0.7-70", sha256="e3432c3b006e5cc6f1292bebd81ebc20044edf1f56c3d27a3497f738eb99f0d3")
    version("0.6-99", sha256="2ef532cba77c5f73803bd34582bef05709705311a0b50e42316e69944567390f")
    version("0.6-60", sha256="55cad759510d247ebbf03a53a46caddadd3bf87584ccf7fcd6dd06d44516b377")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.7-70:")
    depends_on("r-ape@4.0:", type=("build", "run"))
    depends_on("r-ape@5.7:", type=("build", "run"), when="@1.5-1:")
    depends_on("r-maps", type=("build", "run"))
    depends_on("r-clustergeneration", type=("build", "run"))
    depends_on("r-coda", type=("build", "run"))
    depends_on("r-combinat", type=("build", "run"))
    depends_on("r-deoptim", type=("build", "run"), when="@2.2-0:")
    depends_on("r-doparallel", type=("build", "run"), when="@1.5-1:")
    depends_on("r-expm", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"), when="@1.5-1:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-mnormt", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-numderiv", type=("build", "run"))
    depends_on("r-optimparallel", type=("build", "run"), when="@1.2-0:")
    depends_on("r-phangorn@2.3.1:", type=("build", "run"))
    depends_on("r-scatterplot3d", type=("build", "run"))

    depends_on("r-animation", type=("build", "run"), when="@:0.6-99")
    depends_on("r-gtools", type=("build", "run"), when="@0.6-99:0.7-70")
    depends_on("r-plotrix", type=("build", "run"), when="@:2.0-2")
