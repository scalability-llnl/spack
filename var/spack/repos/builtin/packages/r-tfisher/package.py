# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTfisher(RPackage):
    """Optimal Thresholding Fisher's P-Value Combination Method.

    We provide the cumulative distribution function (CDF), quantile, and
    statistical power calculator for a collection of thresholding Fisher's
    p-value combination methods, including Fisher's p-value combination method,
    truncated product method and, in particular, soft-thresholding Fisher's
    p-value combination method which is proven to be optimal in some context of
    signal detection. The p-value calculator for the omnibus version of these
    tests are also included. For reference, please see Hong Zhang and Zheyang
    Wu. "TFisher Tests: Optimal and Adaptive Thresholding for Combining
    p-Values", submitted."""

    cran = "TFisher"

    version("0.2.0", sha256="bd9b7484d6fba0165841596275b446f85ba446d40e92f3b9cb37381a3827e76f")

    depends_on("r-sn", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
