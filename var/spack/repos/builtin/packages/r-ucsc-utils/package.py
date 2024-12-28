# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUcscUtils(RPackage):
    """Low-level utilities to retrieve data from the UCSC Genome Browser."""

    bioc = "UCSC.utils"

    version("1.3.0", commit="1fe2970955d486197d62791b34d0984656c5edf5")

    depends_on("r-httr", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
