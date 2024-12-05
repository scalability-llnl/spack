# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RShortread(RPackage):
    """FASTQ input and manipulation.

    This package implements sampling, iteration, and input of FASTQ files.
    The package includes functions for filtering and trimming reads, and for
    generating a quality assessment report. Data are represented as
    DNAStringSet-derived objects, and easily manipulated for a diversity of
    purposes. The package also contains legacy support for early single-end,
    ungapped alignment formats."""

    bioc = "ShortRead"

    version("1.58.0", commit="433d18266b141ddcc9dc590f5244163a04efebe3")
    version("1.56.0", commit="df25d0872d52aac3610998abda0d7bfd37298726")
    version("1.54.0", commit="a1082a335120860d019aa0065a975d41890351f7")
    version("1.52.0", commit="4d7304d7b5a0ca5c904c0b919d6c95599db72a39")
    version("1.48.0", commit="ba44cd2517bc0e6f46d2cfcfce393f86eec814d0")
    version("1.42.0", commit="daa2576a48278460caf87f42c022c796652f4908")
    version("1.40.0", commit="0cbe4b62b0be4c5f2e2670da17493423446e008f")
    version("1.38.0", commit="e9498f04b7b4bf0212bbb10ec7e3de2d7699f4bf")
    version("1.36.1", commit="176c34eddf4a416d30c69cb4ac197141ba42e66f")
    version("1.34.2", commit="25daac63b301df66a8ef6e98cc2977522c6786cd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r-biocgenerics@0.22.1:", type=("build", "run"))
    depends_on("r-biocgenerics@0.23.3:", type=("build", "run"), when="@1.36.1:")
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-biostrings@2.37.1:", type=("build", "run"))
    depends_on("r-biostrings@2.47.6:", type=("build", "run"), when="@1.38.0:")
    depends_on("r-rsamtools@1.21.4:", type=("build", "run"))
    depends_on("r-rsamtools@1.31.2:", type=("build", "run"), when="@1.38.0:")
    depends_on("r-genomicalignments@1.5.4:", type=("build", "run"))
    depends_on("r-genomicalignments@1.15.6:", type=("build", "run"), when="@1.38.0:")
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-s4vectors@0.13.8:", type=("build", "run"))
    depends_on("r-s4vectors@0.17.25:", type=("build", "run"), when="@1.38.0:")
    depends_on("r-iranges@2.3.7:", type=("build", "run"))
    depends_on("r-iranges@2.13.12:", type=("build", "run"), when="@1.38.0:")
    depends_on("r-genomeinfodb@1.1.19:", type=("build", "run"))
    depends_on("r-genomeinfodb@1.15.2:", type=("build", "run"), when="@1.38.0:")
    depends_on("r-genomicranges@1.21.6:", type=("build", "run"))
    depends_on("r-genomicranges@1.31.8:", type=("build", "run"), when="@1.38.0:")
    depends_on("r-hwriter", type=("build", "run"))
    depends_on("r-zlibbioc", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-latticeextra", type=("build", "run"))
    depends_on("r-xvector", type=("build", "run"))
    depends_on("r-rhtslib", type=("build", "run"), when="@1.48.0:")
    depends_on("zlib-api")
