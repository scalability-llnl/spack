# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRrpp(RPackage):
    """Linear Model Evaluation with Randomized Residuals in a Permutation Procedure

    Linear model calculations are made for many random versions of data. Using
    residual randomization in a permutation procedure, sums of squares are
    calculated over many permutations to generate empirical probability
    distributions for evaluating model effects. This packaged is described by
    Collyer & Adams (2018) <doi:10.1111/2041-210X.13029>. Additionally,
    coefficients, statistics, fitted values, and residuals generated over many
    permutations can be used for various procedures including pairwise tests,
    prediction, classification, and model comparison. This package should
    provide most tools one could need for the analysis of high-dimensional
    data, especially in ecology and evolutionary biology, but certainly other
    fields, as well."""

    homepage = "https://github.com/mlcollyer/RRPP"
    url      = "https://cloud.r-project.org/src/contrib/RRPP_0.3.0.tar.gz"
    list_url = "https://cron.r-project.org/src/contrib/Archive/RRPP"

    version('0.6.2', sha256='f8ffa318d806184c0e65929ea1b8b6a88bb9e45f77db2da5a83c6fe550b084dc')
    version('0.4.2', sha256='21a4ebb549d21f66ee9107adf762eee630e478bc740f232f384ba1a6b1cd3bf4')
    version('0.4.1', sha256='d7cd3b089240d7f7e13f65f0259487669a378ffae062aee33d4dc6ab0f86f899')
    version('0.3.0', sha256='34fea6ce7a78e4f38398d3b99585bab11a8171bc8b9a4e461b6d984ed1373739')

    depends_on('r@3.5.0:', when='@0.6.2:', type=('build', 'run'))
    depends_on('r-ape', when='@0.6.2:', type=('build', 'run'))
