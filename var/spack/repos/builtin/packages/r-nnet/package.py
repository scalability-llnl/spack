# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNnet(RPackage):
    """Feed-Forward Neural Networks and Multinomial Log-Linear Models.

    Software for feed-forward neural networks with a single hidden layer, and
    for multinomial log-linear models."""

    cran = "nnet"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("7.3-19", sha256="a9241f469270d3b03bbab7dc0d3c6a06a84010af16ba82fd3bd6660b35382ce7")
    version("7.3-18", sha256="d29aebfb5cb00071eecf754d55db5d474a6fda88860df5c9d31ba89aa8d9e3d0")
    version("7.3-17", sha256="ee750bb8164aa058edf93823af987ab2c7ec64128dce2abeaae1b7d3661e9a67")
    version("7.3-14", sha256="5d1b9e9764d74d16c651f18f949aa4e9e2995ba64633cbfa2c6a7355ae30f4af")
    version("7.3-12", sha256="2723523e8581cc0e2215435ac773033577a16087a3f41d111757dd96b8c5559d")

    depends_on("r@2.14:", type=("build", "run"))
    depends_on("r@3.0.0:", type=("build", "run"), when="@7.3-14:")
