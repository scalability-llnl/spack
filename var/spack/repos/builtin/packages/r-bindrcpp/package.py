# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBindrcpp(RPackage):
    """An 'Rcpp' Interface to Active Bindings.

    Provides an easy way to fill an environment with active bindings that call
    a C++ function."""

    cran = "bindrcpp"

    license("MIT")

    version("0.2.3", sha256="662dae785aee715855415f4e743281ccbf0832e426084dc2f0ca9c9c908ec9fa")
    version("0.2.2", sha256="48130709eba9d133679a0e959e49a7b14acbce4f47c1e15c4ab46bd9e48ae467")
    version("0.2", sha256="d0efa1313cb8148880f7902a4267de1dcedae916f28d9a0ef5911f44bf103450")

    depends_on("r-rcpp@0.12.16:", type=("build", "run"))
    depends_on("r-bindr@0.1.1:", type=("build", "run"))
    depends_on("r-plogr", type=("build", "run"))
