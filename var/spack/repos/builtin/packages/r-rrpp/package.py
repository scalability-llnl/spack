# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRrpp(RPackage):
    """Linear Model Evaluation with Randomized Residuals in a Permutation
    Procedure.

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

    cran = "RRPP"

    version("2.0.3", sha256="ff70976d4656c39bb02d842668c4d283bc2a26294d3aa2c6590f86a87fd8a2b5")
    version("1.3.1", sha256="50c7d4b20fb84088b0440c2f55ed146bcb35b0d9dda8581dca28e30b2fecbcd5")
    version("1.2.3", sha256="6eee638af94d69d4dd471a5e01243622dedef3c0c95b3363e21e8e11f0ea564c")
    version("1.1.2", sha256="2b563f3db9e349abe481444f48a1a3e6bc1154de8259b7a7060ab588287e80c0")
    version("0.6.2", sha256="f8ffa318d806184c0e65929ea1b8b6a88bb9e45f77db2da5a83c6fe550b084dc")
    version("0.4.2", sha256="21a4ebb549d21f66ee9107adf762eee630e478bc740f232f384ba1a6b1cd3bf4")
    version("0.4.1", sha256="d7cd3b089240d7f7e13f65f0259487669a378ffae062aee33d4dc6ab0f86f899")
    version("0.3.0", sha256="34fea6ce7a78e4f38398d3b99585bab11a8171bc8b9a4e461b6d984ed1373739")

    depends_on("r@3.5.0:", type=("build", "run"), when="@0.6.2:")
    depends_on("r@4.4.0:", type=("build", "run"), when="@2.0.3:")
    depends_on("r-ape", type=("build", "run"), when="@0.6.2:")
    depends_on("r-ggplot2", type=("build", "run"), when="@1.1.2:")
    depends_on("r-matrix", type=("build", "run"), when="@1.1.2:")
