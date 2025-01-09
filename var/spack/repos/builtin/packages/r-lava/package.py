# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLava(RPackage):
    """Latent Variable Models.

    A general implementation of Structural Equation Models with latent
    variables (MLE, 2SLS, and composite likelihood estimators) with both
    continuous, censored, and ordinal outcomes (Holst and Budtz-Joergensen
    (2013) <doi:10.1007/s00180-012-0344-y>). Mixture latent variable models and
    non-linear latent variable models (Holst and Budtz-Joergensen (2019)
    <doi:10.1093/biostatistics/kxy082>). The package also provides methods for
    graph exploration (d-separation, back-door criterion), simulation of
    general non-linear latent variable models, and estimation of influence
    functions for a broad range of statistical models."""

    cran = "lava"

    license("GPL-3.0-only")

    version("1.8.0", sha256="8db996eeca012c58736f2d3b97f569c03e9361e20f31513c090a9386eb87e87f")
    version("1.7.2.1", sha256="d42b1f5c7e4e76718e4f014c44608295f82b5de0eb25ce8e9b35c40c7839ef2e")
    version("1.7.0", sha256="3078da69f3828812bcd093acc2d1cd2c8cbc8480d81da222ae49a55bcb2e5e24")
    version("1.6.10", sha256="7a88f8a885872e2abb3011c446e9e1c4884cd4dbe6ab4cfe9207538e5560232e")
    version("1.6.8.1", sha256="6d243fc86c67c78ff4763502d84ff2f0889c2e55d1a59afefb7a762887473ffa")
    version("1.6.6", sha256="7abc84dd99cce450a45ac4f232812cde3a322e432da3472f43b057fb5c59ca59")
    version("1.6.4", sha256="41c6eeb96eaef9e1bfb04b31f7203e250a5ea7e7860be4d95f7f96f2a8644718")
    version("1.4.7", sha256="d5cbd4835a94855478efb93051eece965db116ead203f4dd4e09d9a12d52f4bf")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-cli", type=("build", "run"), when="@1.7.4:")
    depends_on("r-future-apply", type=("build", "run"), when="@1.6.10:")
    depends_on("r-progressr", type=("build", "run"), when="@1.6.10:")
    depends_on("r-numderiv", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-squarem", type=("build", "run"), when="@1.6.0:")
