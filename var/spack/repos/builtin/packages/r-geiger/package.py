# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeiger(RPackage):
    """Analysis of Evolutionary Diversification.

    Methods for fitting macroevolutionary models to phylogenetic trees  Pennell
    (2014) <doi:10.1093/bioinformatics/btu181>."""

    cran = "geiger"

    license("GPL-2.0-or-later")

    version("2.0.11", sha256="dcc5a0a988439110078867e0aaf09b048e27db7f02e4cbdfe35783611fde3f69")
    version("2.0.10", sha256="2895cfb73fb91764be2ec3f931e4f3b2e75ae00a1431af4b40dc90e7c0693be0")
    version("2.0.9", sha256="c8c8c871b4eb03ba1dc2fd49db304741b16ede99fe49bb5f9b2c220b9e2a8066")
    version("2.0.7", sha256="d200736c4ad7ed4bc55a13e7d0126ddc7fed88e245cd5706d4692aaa437e9596")
    version("2.0.6.2", sha256="9153047b608d652821251206d1450bb3f517c8884379f498a695315574ae001d")
    version("2.0.6.1", sha256="2a95e20a3a90c096343b014344dd97e699e954da99c151c17fc6c245c77dba0b")
    version("2.0.6", sha256="e13b2c526378eaf9356b00bbe21b3c2c956327f8062fed638ccc1f49591c3eff")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@2.15.0:", type=("build", "run"))
    depends_on("r-ape@3.0-6:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))
    depends_on("r-subplex", type=("build", "run"))
    depends_on("r-desolve@1.7:", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-coda", type=("build", "run"))
    depends_on("r-ncbit", type=("build", "run"))
    depends_on("r-colorspace", type=("build", "run"))
    depends_on("r-phytools@0.7.31:", type=("build", "run"), when="@2.0.7:")
    depends_on("r-phytools@1.5-1:", type=("build", "run"), when="@2.0.11:")
