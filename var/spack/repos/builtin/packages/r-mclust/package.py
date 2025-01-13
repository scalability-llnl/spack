# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMclust(RPackage):
    """Gaussian Mixture Modelling for Model-Based Clustering, Classification,
    and Density Estimation.

    Gaussian finite mixture models fitted via EM algorithm for model-based
    clustering, classification, and density estimation, including Bayesian
    regularization, dimension reduction for visualisation, and resampling-based
    inference."""

    cran = "mclust"

    license("GPL-2.0-or-later")

    version("6.1.1", sha256="ddd7018e5e6ea7f92c7fc9872b391491b7e91c2cd89ef1dcaf4408afb5116775")
    version("6.0.0", sha256="de7c306ecba1ef0f4e4a56c748ce08149417496b711beefb032d561a4c28122a")
    version("5.4.10", sha256="2a1bbbf3c4a17df08d1ba8bc4d3c6d9c7241ed5fd68b8aabe660115597b60672")
    version("5.4.9", sha256="65f123c6af86cf5eb511c81ae0eafa60da7b2085bfea1a08bdc3116081da9568")
    version("5.4.7", sha256="45f5a666caee5bebd3160922b8655295a25e37f624741f6574365e4ac5a14c23")
    version("5.4.5", sha256="75f2963082669485953e4306ffa93db98335ee6afdc1318b95d605d56cb30a72")
    version("5.4.4", sha256="ccc31b0ad445e121a447b04988e73232a085c506fcc7ebdf11a3e0754aae3e0d")
    version("5.3", sha256="2b1b6d8266ae16b0e96f118df81559f208a568744a7c105af9f9abf1eef6ba40")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.0:", type=("build", "run"), when="@6.0.0:")
