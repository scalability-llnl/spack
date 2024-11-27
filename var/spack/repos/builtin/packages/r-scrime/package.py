# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScrime(RPackage):
    """Analysis of High-Dimensional Categorical Data Such as SNP Data.

    Tools for the analysis of high-dimensional data developed/implemented at
    the group "Statistical Complexity Reduction In Molecular Epidemiology"
    (SCRIME). Main focus is on SNP data. But most of the functions can also be
    applied to other types of categorical data."""

    cran = "scrime"

    license("GPL-2.0-only")

    version("1.3.5", sha256="5d97d3e57d8eb30709340fe572746029fd139456d7a955421c4e3aa75d825578")
