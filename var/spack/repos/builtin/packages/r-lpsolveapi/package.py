# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLpsolveapi(RPackage):
    """R Interface to 'lp_solve' Version 5.5.2.0.

    The lpSolveAPI package provides an R interface to 'lp_solve', a Mixed
    Integer Linear Programming (MILP) solver with support for pure linear,
    (mixed) integer/binary, semi-continuous and special ordered sets (SOS)
    models."""

    cran = "lpSolveAPI"

    version(
        "5.5.2.0-17.12", sha256="4f00a9d27055ddf3e2a4b0a529b720861b9f916f2ceb1fe0b71e4c52da5b70ef"
    )
    version(
        "5.5.2.0-17.9", sha256="7b52ecf3f1174f771fe24e62502be6d31acc3e48a12473e35ad0a89fc2517811"
    )
    version(
        "5.5.2.0-17.8", sha256="24346bbdfe86a955e0f831c42e14c0ad6f446e4cbd07b82ce81a824d7717569e"
    )
    version(
        "5.5.2.0-17.7", sha256="9ebc8e45ad73eb51e0b25049598a5bc758370cf89508e2328cf4bd93d68d55bb"
    )
