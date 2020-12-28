# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRrpp(RPackage):
    """Linear model calculations are made for many random versions of data.

       Using residual randomization in a permutation procedure, sums of
       squares are calculated over many permutations to generate empirical
       probability distributions for evaluating model effects. This method
       is described by Collyer, Sekora, & Adams (2015)
       <doi:10.1038/hdy.2014.75>. Additionally, coefficients, statistics,
       fitted values, and residuals generated over many permutations can be
       used for various procedures including pairwise tests, prediction,
       classification, and model comparison. This package should provide
       most tools one could need for the analysis of high-dimensional data,
       especially in ecology and evolutionary biology, but certainly
       other fields, as well."""

    homepage = "https://github.com/mlcollyer/RRPP"
    url      = "https://cloud.r-project.org/src/contrib/RRPP_0.3.0.tar.gz"
    list_url = "https://cron.r-project.org/src/contrib/Archive/RRPP"

    version('0.4.2', sha256='21a4ebb549d21f66ee9107adf762eee630e478bc740f232f384ba1a6b1cd3bf4')
    version('0.4.1', sha256='d7cd3b089240d7f7e13f65f0259487669a378ffae062aee33d4dc6ab0f86f899')
    version('0.3.0', sha256='34fea6ce7a78e4f38398d3b99585bab11a8171bc8b9a4e461b6d984ed1373739')
