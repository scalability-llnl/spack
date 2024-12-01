# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDose(RPackage):
    """Disease Ontology Semantic and Enrichment analysis.

    This package implements five methods proposed by Resnik, Schlicker,
    Jiang, Lin and Wang respectively for measuring semantic similarities
    among DO terms and gene products. Enrichment analyses including
    hypergeometric model and gene set enrichment analysis are also
    implemented for discovering disease associations of high-throughput
    biological data."""

    bioc = "DOSE"

    version("3.26.0", commit="9c91fb45a2ab9a875a6a7259610b7d5bc86933f6")
    version("3.24.1", commit="a78995d3b12bd4baabb69c497102687814cd4c68")
    version("3.22.1", commit="6b711a0f076a9fefcb00ddef66e8f198039e6dfa")
    version("3.22.0", commit="242ac1b746c44fbbf281fbe6e5e4424a8dc74375")
    version("3.20.1", commit="bf434f24d035217822cb1b0ab08a486b9a53edb4")
    version("3.16.0", commit="a534a4f2ef1e54e8b92079cf1bbedb5042fd90cd")
    version("3.10.2", commit="5ea51a2e2a04b4f3cc974cecb4537e14efd6a7e3")
    version("3.8.2", commit="4d3d1ca710aa7e4288a412c8d52b054b86a57639")
    version("3.6.1", commit="f2967f0482cea39222bfd15767d0f4a5994f241b")
    version("3.4.0", commit="dabb70de1a0f91d1767601e871f2f1c16d29a612")
    version("3.2.0", commit="71f563fc39d02dfdf65184c94e0890a63b96b86b")

    depends_on("r@3.3.1:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@3.6.1:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.16.0:")
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-hdo-db", type=("build", "run"), when="@3.24.1:")
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-fgsea", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-gosemsim@2.0.0:", type=("build", "run"))
    depends_on("r-gosemsim@2.23.1:", type=("build", "run"), when="@3.24.1:")
    depends_on("r-qvalue", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))

    depends_on("r-s4vectors", type=("build", "run"), when="@:3.10.2")
    depends_on("r-scales", type=("build", "run"), when="@3.2.0:3.4.0")
    depends_on("r-rvcheck", type=("build", "run"), when="@3.4.0")
    depends_on("r-igraph", type=("build", "run"), when="@3.2.0:3.4.0")
    depends_on("r-do-db", type=("build", "run"), when="@:3.22.1")
