# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGensa(RPackage):
    """Generalized Simulated Annealing.

    Performs search for global minimum of a very complex non-linear objective
    function with a very large number of optima."""

    cran = "GenSA"

    version("1.1.14", sha256="66e455bb0e66d3c04af84d9dddc9b89f40b4cf9fe9ad1cf0714bcf30aa1b6837")
    version("1.1.8", sha256="375e87541eb6b098584afccab361dc28ff09d03cf1d062ff970208e294eca216")
    version("1.1.7", sha256="9d99d3d0a4b7770c3c3a6de44206811272d78ab94481713a8c369f7d6ae7b80f")

    depends_on("r@2.12.0:", type=("build", "run"))
