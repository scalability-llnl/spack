# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIrlba(RPackage):
    """Fast Truncated Singular Value Decomposition and Principal Components
    Analysis for Large Dense and Sparse Matrices.

    Fast and memory efficient methods for truncated singular value
    decomposition and principal components analysis of large sparse and dense
    matrices."""

    cran = "irlba"

    license("GPL-3.0-only")

    version("2.3.5.1", sha256="2cfe6384fef91c223a9920895ce89496f990d1450d731e44309fdbec2bb5c5cf")
    version("2.3.5", sha256="26fc8c0d36460e422ab77f43a597b8ec292eacd452628c54d34b8bf7d5269bb9")
    version("2.3.3", sha256="6ee233697bcd579813bd0af5e1f4e6dd1eea971e8919c748408130d970fef5c0")
    version("2.3.2", sha256="3fdf2d8fefa6ab14cd0992740de7958f9f501c71aca93229f5eb03c54558fc38")
    version("2.1.2", sha256="5183e8dd7943df11c0f44460566adf06c03d5320f142699298f516d423b06ce1")
    version("2.0.0", sha256="15f8d6c1107d6bb872411efd61e6077d9d7ac826f4da2d378999889a7b1ebabe")

    depends_on("c", type="build")  # generated

    depends_on("r@3.6.2:", type=("build", "run"), when="@2.3.5:")
    depends_on("r-matrix", type=("build", "run"))
