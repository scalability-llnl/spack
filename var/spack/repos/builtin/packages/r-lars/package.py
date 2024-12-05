# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLars(RPackage):
    """Least Angle Regression, Lasso and Forward Stagewise.

    Efficient procedures for fitting an entire lasso sequence with the cost
    of a single least squares fit."""

    cran = "lars"

    license("GPL-2.0-only")

    version("1.3", sha256="c69e6a8da6a3344c0915dd1fd4c78fec5cdf50c62cf6297476e9bb7dc10b549d")
    version("1.2", sha256="64745b568f20b2cfdae3dad02fba92ebf78ffee466a71aaaafd4f48c3921922e")
    version("1.1", sha256="a8e4a0efb9ca6760dec1cadf395d9a805508455a2c3ced18cc53d9b8fa70cdc0")
    version("0.9-8", sha256="8c64cb31073ea0785346bb716485da8db2fae14153a52e5a8d151bc9cb4906e5")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
