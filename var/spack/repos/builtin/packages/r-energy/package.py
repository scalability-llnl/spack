# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REnergy(RPackage):
    """E-Statistics: Multivariate Inference via the Energy of Data.

    E-statistics (energy) tests and statistics for multivariate and univariate
    inference, including distance correlation, one-sample, two-sample, and
    multi-sample tests for comparing multivariate distributions, are
    implemented. Measuring and testing multivariate independence based on
    distance correlation, partial distance correlation, multivariate
    goodness-of-fit tests, k-groups and hierarchical clustering based on energy
    distance, testing for multivariate normality, distance components (disco)
    for non-parametric  analysis of structured data, and other energy
    statistics/methods are implemented."""

    cran = "energy"

    license("GPL-2.0-or-later")

    version("1.7-11", sha256="c29f8fb000c979d2504f6f6d3a99c773004f77d58793e7e2a5766155272b6511")
    version("1.7-10", sha256="543de4875c46cc90e711e71c45b082d962fbb5158a094f9f10d37d3f57e1bea7")
    version("1.7-9", sha256="68d0e0ed99f5a8a03858603ed36010a2f67b87a947dbcc65a9da2e08a2d3bad9")
    version("1.7-8", sha256="de08e8de037bb30068bbf0c1880b153a586d342304681f4ba103ab808c7f4789")
    version("1.7-7", sha256="67b88fb33ee6e7bec2e4fe356a4efd36f70c3cf9b0ebe2f6d9da9ec96de9968f")
    version("1.7-6", sha256="900edbb28e1f1bccd78580828470628cf75eb6333b63e1a58e4da7fc5c5fa89a")
    version("1.7-5", sha256="24c2cf080939f8f56cd9cda06d2dfc30d0389cd3ec7250af4f9a09a4c06b6996")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.1:", type=("build", "run"), when="@1.7-11:")
    depends_on("r-rcpp@0.12.6:", type=("build", "run"))
    depends_on("r-boot", type=("build", "run"))
    depends_on("r-gsl", type=("build", "run"), when="@1.7-8:")
