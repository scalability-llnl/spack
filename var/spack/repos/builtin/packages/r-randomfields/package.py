# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRandomfields(RPackage):
    """Simulation and Analysis of Random Fields.

    Methods for the inference on and the simulation of Gaussian fields are
    provided. Furthermore, methods for the simulation of extreme value random
    fields are provided. Main geostatistical parts are based among others on
    the books by Christian Lantuejoul <doi:10.1007/978-3-662-04808-5>."""

    cran = "RandomFields"

    version("3.3.14", sha256="242600b9bf93af9d49a06c00ff2398054a882d644a4653ea348533410c3db930")
    version("3.3.13", sha256="dbf82a8a39a79ca1b53665c2375cdd58f7accb38062063bbd9854d13493d3f49")
    version("3.3.8", sha256="8a08e2fdae428e354a29fb6818ae781cc56235a6849a0d29574dc756f73199d0")
    version("3.3.6", sha256="51b7bfb4e5bd7fd0ce1207c77f428508a6cd3dfc9de01545a8724dfd9c050213")
    version("3.3.4", sha256="a340d4f3ba7950d62acdfa19b9724c82e439d7b1a9f73340124038b7c90c73d4")
    version("3.1.50", sha256="2d6a07c3a716ce20f9c685deb59e8fcc64fd52c8a50b0f04baf451b6b928e848")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.3.8:")
    depends_on("r-sp", type=("build", "run"))
    depends_on("r-randomfieldsutils@0.5.1:", type=("build", "run"))
    depends_on("r-randomfieldsutils@0.5.5:", type=("build", "run"), when="@3.3.13:")
    depends_on("r-randomfieldsutils@1.1:", type=("build", "run"), when="@3.3.14:")
