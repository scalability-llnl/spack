# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSimpleaffy(RPackage):
    """Very simple high level analysis of Affymetrix data.

    Provides high level functions for reading Affy .CEL files, phenotypic
    data, and then computing simple things with it, such as t-tests, fold
    changes and the like. Makes heavy use of the affy library. Also has some
    basic scatter plot functions and mechanisms for generating high
    resolution journal figures..."""

    bioc = "simpleaffy"

    license("Unlicense")

    version("2.66.0", commit="902db69e4ea4b6d306f0c744d3be600f1418ebc9")
    version("2.60.0", commit="b32b5e7d5c65e43c10f98ab8684a1086a06d04f9")
    version("2.58.0", commit="70cf1199bad620f60eaa288279632110bb571200")
    version("2.56.0", commit="a05d768180b8713ad9e1dc46d491b7ef389b299d")
    version("2.54.0", commit="6876e028d412b14504ad3915cbec1a189e9c6478")
    version("2.52.0", commit="f2b43fb9b8e6fa4c03fe28b4efb3144a0a42a385")

    depends_on("c", type="build")  # generated

    depends_on("r@2.0.0:", type=("build", "run"))
    depends_on("r-biocgenerics@0.1.12:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-affy@1.33.6:", type=("build", "run"))
    depends_on("r-genefilter", type=("build", "run"))
    depends_on("r-gcrma", type=("build", "run"))
