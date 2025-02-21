# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPspline(RPackage):
    """Penalized Smoothing Splines.

    Smoothing splines with penalties on order m derivatives."""

    cran = "pspline"

    license("custom")

    version("1.0-20", sha256="eaa7cd9b870d5d10cf457c435ebcbe698ba0d463e3a996fbe758a4b57b93eb8a")
    version("1.0-19", sha256="ba55bf193f1df9785a0e13b7ef727d5fd2415b318cd6a26b48a2db490c4dfe40")
    version("1.0-18", sha256="f71cf293bd5462e510ac5ad16c4a96eda18891a0bfa6447dd881c65845e19ac7")

    depends_on("r@2.0.0:", type=("build", "run"))
