# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBridgesampling(RPackage):
    """Bridge Sampling for Marginal Likelihoods and Bayes Factors.

    Provides functions for estimating marginal likelihoods, Bayes factors,
    posterior model probabilities, and normalizing constants in general, via
    different versions of bridge sampling (Meng & Wong, 1996,
    <http://www3.stat.sinica.edu.tw/statistica/j6n4/j6n43/j6n43.htm>). Gronau,
    Singmann, & Wagenmakers (2020) <doi:10.18637/jss.v092.i10>."""

    cran = "bridgesampling"

    license("GPL-2.0-or-later")

    version("1.1-2", sha256="54ecd39aa2e36d4d521d3d36425f9fe56a3f8547df6048c814c5931d790f3e6b")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-brobdingnag", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-coda", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
