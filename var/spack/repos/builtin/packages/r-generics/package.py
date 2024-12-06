# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenerics(RPackage):
    """Common S3 Generics not Provided by Base R Methods Related to Model
    Fitting.

    In order to reduce potential package dependencies and conflicts, generics
    provides a number of commonly used S3 generics."""

    cran = "generics"

    license("MIT")

    version("0.1.3", sha256="75046163bfa8b8a4f4214c1b689e796207f6447182f2e5062cf570302387d053")
    version("0.1.2", sha256="63eab37a9148f820ce2d67bda3dab6dedb9db6890baa5284949c39ab1b4c5898")
    version("0.1.1", sha256="a2478ebf1a0faa8855a152f4e747ad969a800597434196ed1f71975a9eb11912")
    version("0.1.0", sha256="ab71d1bdbb66c782364c61cede3c1186d6a94c03635f9af70d926e2c1ac88763")
    version("0.0.2", sha256="71b3d1b719ce89e71dd396ac8bc6aa5f1cd99bbbf03faff61dfbbee32fec6176")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"), when="@0.1.1:")
