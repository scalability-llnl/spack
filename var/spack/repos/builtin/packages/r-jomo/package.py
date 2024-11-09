# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJomo(RPackage):
    """Multilevel Joint Modelling Multiple Imputation.

    Similarly to Schafer's package 'pan', 'jomo' is a package for multilevel
    joint modelling multiple imputation (Carpenter and Kenward, 2013)
    <doi:10.1002/9781119942283>. Novel aspects of 'jomo' are the possibility of
    handling binary and categorical data through latent normal variables, the
    option to use cluster-specific covariance matrices and to impute compatibly
    with the substantive model."""

    cran = "jomo"

    license("GPL-2.0-only")

    version("2.7-6", sha256="3ffa2a5521d4969fe77b23cd3ab201afdf8db3f8f708b1276c33083c01d7e2da")
    version("2.7-4", sha256="2d25bc248dc1b931e6c19636197cd6f58fb00f5e1102ed3c04084c71d03d93fd")
    version("2.7-3", sha256="9d3987f3a73d305f3ab6fc66efc04a196a7eb8b65e20c411131dc17af51f0063")
    version("2.7-2", sha256="3962d5cbecc60e72670329dbef0dd74303080f5ea2a79c91e27f75db99ba6ce9")
    version("2.6-9", sha256="b90f47071e62b8863b00b1ae710a56ae6efbfe2baeb9963f8a91a10d6183cc9b")
    version("2.6-7", sha256="6e83dab51103511038a3e9a3c762e00cc45ae7080c0a0f64e37bcea8c488db53")
    version("2.6-2", sha256="67496d6d69ddbe9a796789fd8b3ac32cada09a81cf5a8e7b925a21e085e2d87f")

    depends_on("c", type="build")  # generated

    depends_on("r-lme4", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"), when="@2.6-7:")
    depends_on("r-ordinal", type=("build", "run"), when="@2.6-7:")
    depends_on("r-tibble", type=("build", "run"), when="@2.7-3:")
