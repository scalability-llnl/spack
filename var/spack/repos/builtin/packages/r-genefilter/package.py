# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenefilter(RPackage):
    """Methods for filtering genes from high-throughput experiments.

    Some basic functions for filtering genes."""

    bioc = "genefilter"

    version("1.82.0", commit="1ee4bdc65b0144853211354f8fabf8b497d9a565")
    version("1.80.0", commit="14fbc2d776916e572583e3c268ea9ba60ed60a9a")
    version("1.78.0", commit="2f574388971641d3a71858f5c34606c04fcd2ba2")
    version("1.76.0", commit="8d630fd25f0d2a4101e05e123c3959591203a7ea")
    version("1.72.1", commit="b01b00a766982ef7d80b90a252085c8c4f085e1b")
    version("1.72.0", commit="8cb0b2e73531a417d53e5625bcf436265cdbe101")
    version("1.66.0", commit="1c4c471ccca873bf92dcf0b50f611eaa64c4f0cf")
    version("1.64.0", commit="82e91b7751bae997b9c898c219ea201fd02a8512")
    version("1.62.0", commit="eb119894f015c759f93f458af7733bdb770a22ad")
    version("1.60.0", commit="c98f695253c330a9380b2b4ffa27f3b7d66773e4")
    version("1.58.1", commit="ace2556049677f60882adfe91f8cc96791556fc2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r-matrixgenerics@1.11.1:", type=("build", "run"), when="@1.82.0:")
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-annotate", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-s4vectors@0.9.42:", type=("build", "run"), when="@:1.66.0")
    depends_on("r-biocgenerics", type=("build", "run"), when="@1.78.0:1.80.0")
    depends_on("r-biocgenerics@0.31.2:", type=("build", "run"), when="@1.68.0:1.80.0")
