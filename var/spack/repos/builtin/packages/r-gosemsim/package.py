# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGosemsim(RPackage):
    """GO-terms Semantic Similarity Measures.

    The semantic comparisons of Gene Ontology (GO) annotations provide
    quantitative ways to compute similarities between genes and gene groups,
    and have became important basis for many bioinformatics analysis
    approaches. GOSemSim is an R package for semantic similarity computation
    among GO terms, sets of GO terms, gene products and gene clusters.
    GOSemSim implemented five methods proposed by Resnik, Schlicker, Jiang,
    Lin and Wang respectively."""

    bioc = "GOSemSim"

    version("2.26.0", commit="ef3d5a7fb37b43603de4f43aa4fecadaa47f93e0")
    version("2.24.0", commit="ed7334f3cf3ac7ce5be76003934c29b598089f4d")
    version("2.22.0", commit="fd74aeba2371ebf9db0595cf18674441bdac9618")
    version("2.20.0", commit="fa82442aaa4ad1a8dacc05ee2c54f5e5e770a794")
    version("2.16.1", commit="92f1d567f3584fe488f434abce87c2e1950081c0")
    version("2.10.0", commit="5db1ecbf2f8d870430d6e587609327d05ba3ad7b")
    version("2.8.0", commit="c8c985b2a814cc2365c7f05b2509205e1b6b7f58")
    version("2.6.2", commit="2ffe78e89276e804306554965fc0799318ec56ed")
    version("2.4.1", commit="0656e845860d14e054670ffc246a1c53f699299c")
    version("2.2.0", commit="247434790e6c8cf99e5643f569390362b8c87c52")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.3.2:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@2.8.0:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@2.16.1:")
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-go-db", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
