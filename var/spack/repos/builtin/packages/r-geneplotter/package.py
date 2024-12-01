# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeneplotter(RPackage):
    """Graphics related functions for Bioconductor.

    Functions for plotting genomic data."""

    bioc = "geneplotter"

    version("1.78.0", commit="a105c51d2f7a097ea33c3aad8f2345e9a51406d3")
    version("1.76.0", commit="4eb6a787d0c66110ec9a7d34fc76b64030fbde5d")
    version("1.74.0", commit="ca819565829eac7a9a98e3cafafd6c06a466fddf")
    version("1.72.0", commit="57a1d830ba7844fda5236af0153d5b5587634f96")
    version("1.68.0", commit="f1fea7e468fb24fdfa93ef4493600a4d8d183f69")
    version("1.62.0", commit="1fbaddde11014b453b131860409f89cd784e8e48")
    version("1.60.0", commit="6723a9fc0730e146187e79c2ddab6a68186dc5ad")
    version("1.58.0", commit="2b3f44804d61a40cfe7eaedf74ac9f5a054f7fde")
    version("1.56.0", commit="881d25aece3dc00cc4280457ffecdc25e93bb1f1")
    version("1.54.0", commit="efdd946e092e44e35fde1eb4bcc5ec1d52090940")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-annotate", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
