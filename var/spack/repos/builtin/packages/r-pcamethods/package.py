# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPcamethods(RPackage):
    """A collection of PCA methods.

    Provides Bayesian PCA, Probabilistic PCA, Nipals PCA, Inverse Non-Linear
    PCA and the conventional SVD PCA. A cluster based method for missing
    value estimation is included for comparison. BPCA, PPCA and NipalsPCA
    may be used to perform PCA on incomplete data as well as for accurate
    missing value estimation. A set of methods for printing and plotting the
    results is also provided. All PCA methods make use of the same data
    structure (pcaRes) to provide a common interface to the PCA results.
    Initiated at the Max-Planck Institute for Molecular Plant Physiology,
    Golm, Germany."""

    bioc = "pcaMethods"

    license("GPL-2.0-or-later")

    version("1.92.0", commit="ecbbc5b96b8fa79342611af8f798dd43c36d6699")
    version("1.90.0", commit="52474bc6d125122e89834328a1a780988349756f")
    version("1.88.0", commit="02fb58d6fe35579b86fb2ebd2eaf92e6b53444d2")
    version("1.86.0", commit="9419cfa18c18dfbd1e1194127fd120ab456c3657")
    version("1.82.0", commit="d500b3363308f1f8ca70625c5cd10cce59b27641")
    version("1.76.0", commit="5db995330ced37dfd5ddad6ad1d90b4815d3127a")
    version("1.74.0", commit="1b8f0a5cdfe3664119d0d7e926a2e0fe7320133c")
    version("1.72.0", commit="1bb8c7d056645e62ee5179f6bb30b6594ebf3bfd")
    version("1.70.0", commit="3368fad48ea930775505fd26e4179d7714d633d8")
    version("1.68.0", commit="c8d7c93dcaf7ef728f3d089ae5d55771b320bdab")

    depends_on("cxx", type="build")  # generated

    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-rcpp@0.11.3:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
