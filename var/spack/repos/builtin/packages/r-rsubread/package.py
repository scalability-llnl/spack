# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRsubread(RPackage):
    """Mapping, quantification and variant analysis of sequencing data"""

    bioc = "Rsubread"

    version("2.16.0", commit="62b92c9ed3fc2be89ed9f29e3db1809d1e115dbc")
    version("2.14.2", commit="863bd98c6523b888da59335a6acb516d2676d412")

    depends_on("c", type="build")  # generated

    depends_on("r", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-r-utils", type=("build", "run"))
    depends_on("zlib-api", type=("build", "run"))
