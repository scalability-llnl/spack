# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAcde(RPackage):
    """Artificial Components Detection of Differentially Expressed Genes.

    This package provides a multivariate inferential analysis method for
    detecting differentially expressed genes in gene expression data. It
    uses artificial components, close to the data's principal components but
    with an exact interpretation in terms of differential genetic
    expression, to identify differentially expressed genes while controlling
    the false discovery rate (FDR). The methods on this package are
    described in the vignette or in the article 'Multivariate Method for
    Inferential Identification of Differentially Expressed Genes in Gene
    Expression Experiments' by J. P. Acosta, L. Lopez-Kleine and S. Restrepo
    (2015, pending publication)."""

    bioc = "acde"

    version("1.30.0", commit="4c16b9fd6c91a433bf1345252e022571c4983cb5")
    version("1.28.0", commit="0edccca7be2475fa2ae3b3c36d0d64924c37b3c0")
    version("1.26.0", commit="dfef9a435062e948efd5eda22942a0d500baa992")
    version("1.24.0", commit="0c3c4d47af7eaff37420032ea5245743a65124cf")
    version("1.20.0", commit="cefb4f2e2b0ef3c5f51944c0ece7a71294020350")
    version("1.14.0", commit="6017c7436a46f186b2a3cea9d2b93274f6dd3417")
    version("1.12.0", commit="f6ce5926ac915c2d73436f47daf7f9791645dad4")
    version("1.10.0", commit="2c303dec45f3c70bf333a6eacae568a08d5ca010")
    version("1.8.0", commit="f7fc3e1dce958445f920d3b28b56abde70bfb9de")
    version("1.6.0", commit="244c81f435a077bf7895ea565fa6695e8b079f67")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r-boot@1.3:", type=("build", "run"))
