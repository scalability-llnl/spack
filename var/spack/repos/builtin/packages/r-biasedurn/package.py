# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiasedurn(RPackage):
    """Biased Urn Model Distributions.

    Statistical models of biased sampling in the form of univariate and
    multivariate noncentral hypergeometric distributions, including Wallenius'
    noncentral hypergeometric distribution and Fisher's noncentral
    hypergeometric distribution (also called extended hypergeometric
    distribution). See vignette("UrnTheory") for explanation of these
    distributions."""

    cran = "BiasedUrn"

    version("2.0.12", sha256="29b3b596431c5364e3be9aae2068adb44a205de31c66ec3fa1ef06a4ab8c5792")
    version("2.0.9", sha256="bac62bbbc3e2417772f8784996a6c2d0857adb42e86e46b1a9703b187a406b09")
    version("2.0.8", sha256="205e7f8da8fba76fbf4bd9d12a027599b685dedecc818aad39de5c51dc47b856")
    version("1.07", sha256="2377c2e59d68e758a566452d7e07e88663ae61a182b9ee455d8b4269dda3228e")
