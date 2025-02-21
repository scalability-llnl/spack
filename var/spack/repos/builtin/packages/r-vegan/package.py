# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVegan(RPackage):
    """Community Ecology Package.

    Ordination methods, diversity analysis and other functions for community
    and vegetation ecologists."""

    cran = "vegan"

    license("GPL-2.0-only")

    version("2.6-6.1", sha256="7d2a5e700a6639bef203d6e35dfe6e8cc1dd7440957334317b61a9dafbb90b60")
    version("2.6-4", sha256="5d8ad4bebe79ae2bbd840a34100cf54c62f089c66ea484a542a201afcba21d06")
    version("2.6-2", sha256="ab77d110c959d19b0c6268ae0c8f78c897e2419eff3f1f7b19c1bb2f8db7c059")
    version("2.5-7", sha256="e63b586951ea7d8b0118811f329c700212892ec1db3b93951603ce1d68aa462a")
    version("2.5-5", sha256="876b5266f29f3034fed881020d16f476e62d145a00cb450a1a213e019e056971")
    version("2.5-4", sha256="5116a440111fca49b5f95cfe888b180ff29a112e6301d5e2ac5cae0e628493e0")
    version("2.4-3", sha256="2556b1281a62e53f32bb57539bc600c00a599d0699867912220535d1a3ebec97")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.1.0:", type=("build", "run"), when="@2.5-1")
    depends_on("r@3.2.0:", type=("build", "run"), when="@2.5-2:")
    depends_on("r@3.4.0:", type=("build", "run"), when="@2.5-5:")
    depends_on("r@4.1.0:", type=("build", "run"), when="@2.6-6:")
    depends_on("r-permute@0.9-0:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-mgcv", type=("build", "run"))
