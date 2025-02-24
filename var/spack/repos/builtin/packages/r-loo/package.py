# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLoo(RPackage):
    """Efficient Leave-One-Out Cross-Validation and WAIC for BayesianModels.

    Efficient approximate leave-one-out cross-validation (LOO) for Bayesian
    models fit using Markov chain Monte Carlo, as  described in Vehtari,
    Gelman, and Gabry (2017)  <doi:10.1007/s11222-016-9696-4>.  The
    approximation uses Pareto smoothed importance sampling (PSIS),  a new
    procedure for regularizing importance weights.  As a byproduct of the
    calculations, we also obtain approximate  standard errors for estimated
    predictive errors and for the comparison  of predictive errors between
    models. The package also provides methods  for using stacking and other
    model weighting techniques to average  Bayesian predictive
    distributions."""

    cran = "loo"

    license("GPL-3.0-or-later")

    version("2.8.0", sha256="aab727a95a2e1c0e5005188e7daa6eba52455fa0c5869130d53cee5a8963244c")
    version("2.6.0", sha256="66da60fdf53a62cbc93797fa696a4cc43bce77f1721dd4bc1a58d25b3f981210")
    version("2.5.1", sha256="866a2f54a4e8726cc3062e27daa8a073e6ac4aeb6719af7845284f7a668745f1")
    version("2.4.1", sha256="bc21fb6b4a93a7e95ee1be57e4e787d731895fb8b4743c26b30b43adee475b50")
    version("2.3.1", sha256="d98de21b71d9d9386131ae5ba4da051362c3ad39e0305af4f33d830f299ae08b")
    version("2.1.0", sha256="1bf4a1ef85d151577ff96d4cf2a29c9ef24370b0b1eb08c70dcf45884350e87d")

    depends_on("r@3.1.2:", type=("build", "run"))

    depends_on("r+X", type=("build", "run"))
    depends_on("r-checkmate", type=("build", "run"))
    depends_on("r-matrixstats@0.52:", type=("build", "run"))
    depends_on("r-posterior@1.5.0:", type=("build", "run"), when="@2.7.0:")
    depends_on("pandoc@1.12.3:")
