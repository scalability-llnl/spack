# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUpsetr(RPackage):
    """A More Scalable Alternative to Venn and Euler Diagrams for Visualizing
    Intersecting Sets.

    Creates visualizations of intersecting sets using a novel matrix design,
    along with visualizations of several common set, element and attribute
    related tasks (Conway 2017) <doi:10.1093/bioinformatics/btx364>."""

    cran = "UpSetR"

    version("1.4.0", sha256="351e5fee64204cf77fd378cf2a2c0456cc19d4d98a2fd5f3dac74b69a505f100")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-gridextra", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
