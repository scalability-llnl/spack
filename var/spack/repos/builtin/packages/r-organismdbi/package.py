# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROrganismdbi(RPackage):
    """Software to enable the smooth interfacing of different database
    packages.

    The package enables a simple unified interface to several annotation
    packages each of which has its own schema by taking advantage of the
    fact that each of these packages implements a select methods."""

    bioc = "OrganismDbi"

    version("1.42.0", commit="29fcd5c47f8c479edac630a8e2a05ec5facb1328")
    version("1.40.0", commit="fac971dabef3b6d2473d2061bc1723e3de59c9d7")
    version("1.38.1", commit="fa8da4dd42ab15e1d21fd9f8286440596d50b1ec")
    version("1.38.0", commit="2ca01830a6ffcd0c0018d2bdbd3de8b4df716771")
    version("1.36.0", commit="3e7a90d248ff09f05ccd381ff921e12373a4b330")
    version("1.32.0", commit="c8100c4fea17bf1b10d4efacc73a7e2866d649e3")
    version("1.26.0", commit="495b4a8f8264d06d827537d43b3c6cc705244bb5")
    version("1.24.0", commit="3428952dc0f267a01e256a1c0873656cfbfde7f8")
    version("1.22.0", commit="24e953eb3847222d8018103b79b9fc72483cc513")
    version("1.20.0", commit="d42e06a24777e5ffb966ad5addb4f46dfffa2269")
    version("1.18.1", commit="ba2d1237256805e935d9534a0c6f1ded07b42e95")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r-biocgenerics@0.15.10:", type=("build", "run"))
    depends_on("r-annotationdbi@1.33.15:", type=("build", "run"))
    depends_on("r-genomicfeatures@1.23.31:", type=("build", "run"))
    depends_on("r-genomicfeatures@1.39.4:", type=("build", "run"), when="@1.32.0:")
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-biocmanager", type=("build", "run"), when="@1.24.0:")
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-genomicranges@1.31.13:", type=("build", "run"), when="@1.22.0:")
    depends_on("r-graph", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-rbgl", type=("build", "run"))
    depends_on("r-dbi", type=("build", "run"))
    depends_on("r-s4vectors@0.9.25:", type=("build", "run"))

    depends_on("r-biocinstaller", type=("build", "run"), when="@:1.22.0")
