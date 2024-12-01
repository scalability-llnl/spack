# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatialpack(RPackage):
    """Tools to assess the association between two spatial processes.

    Tools to assess the association between two spatial processes. Currently,
    several methodologies are implemented: A modified t-test to perform
    hypothesis testing about the independence between the processes, a suitable
    nonparametric correlation coefficient, the codispersion coefficient, and an
    F test for assessing the multiple correlation between one spatial process
    and several others. Functions for image processing and computing the
    spatial association between images are also provided."""

    cran = "SpatialPack"

    version("0.4", sha256="8b7fbc6d9f962d4b982777bfc794b99d827d3f33cc07058372f73dff1210188d")
    version("0.3-8196", sha256="9027e1656db97b721a12f5eda46532c6a99b4a079299b8d12fb57d445b237b4d")
    version("0.3-8", sha256="a0e54b5dee3cd30a634e2d30380fe163942b672073fd909be888803332ed5151")
    version("0.3", sha256="4c80fc1c77bc97fc678e6e201ecf7f0f89dcf3417b3b497a28a3639e9b30bd8a")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.3-8196:")
    depends_on("r-fastmatrix", type=("build", "run"), when="@0.3-8196:")
