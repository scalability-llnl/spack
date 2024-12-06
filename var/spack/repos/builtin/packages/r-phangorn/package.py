# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhangorn(RPackage):
    """Phylogenetic Reconstruction and Analysis.

    Allows for estimation of phylogenetic trees and networks using Maximum
    Likelihood, Maximum Parsimony, distance methods and Hadamard conjugation.
    Offers methods for tree comparison, model selection and visualization of
    phylogenetic networks as described in Schliep et al. (2017)
    <doi:10.1111/2041-210X.12760>."""

    cran = "phangorn"

    license("GPL-2.0-or-later")

    version("2.11.1", sha256="10096ecae03e118aa4dbc60d9866175fad4849c948e004cf10c3868e3feed420")
    version("2.10.0", sha256="d153f87053a1e6eebf46be98fad3f118349008c559a6797b55613629cab85dce")
    version("2.8.1", sha256="6d471410ae29775104a94746936e8c1c54c7273dd289333973ec06dad489dc75")
    version("2.5.5", sha256="c58dc1ace26cb4358619a15da3ea4765dbdde1557acccc5103c85589a7571346")
    version("2.5.3", sha256="a306585a0aabe7360a2adaf9116ae2993fb5ceff641b198f2e01e4329d3768af")
    version("2.3.1", sha256="518c31f5b2c5f0a655d02a3c71b00c30caea2794dfc31f9d63f3d505bd7863eb")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@4.1.0:", type=("build", "run"), when="@2.8.1:")
    depends_on("r-digest", type=("build", "run"), when="@2.10.0:")
    depends_on("r-ape@5.0:", type=("build", "run"))
    depends_on("r-ape@5.5:", type=("build", "run"), when="@2.8.1:")
    depends_on("r-ape@5.6:", type=("build", "run"), when="@2.10.0:")
    depends_on("r-fastmatch", type=("build", "run"))
    depends_on("r-generics", type=("build", "run"), when="@2.10.0:")
    depends_on("r-igraph@1.0:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-quadprog", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))

    depends_on("r-rcpp@0.12.0:", type=("build", "run"), when="@:2.5.5")
    depends_on("r-magrittr", type=("build", "run"), when="@:2.5.5")
