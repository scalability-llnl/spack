# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenomicranges(RPackage):
    """Representation and manipulation of genomic intervals.

    The ability to efficiently represent and manipulate genomic annotations
    and alignments is playing a central role when it comes to analyzing
    high-throughput sequencing data (a.k.a. NGS data). The GenomicRanges
    package defines general purpose containers for storing and manipulating
    genomic intervals and variables defined along a genome. More specialized
    containers for representing and manipulating short alignments against a
    reference genome, or a matrix-like summarization of an experiment, are
    defined in the GenomicAlignments and SummarizedExperiment packages,
    respectively. Both packages build on top of the GenomicRanges
    infrastructure."""

    bioc = "GenomicRanges"

    version("1.52.0", commit="883f125ea593099293dc808ec2188be3cbdbd3a7")
    version("1.50.1", commit="6b3fb388ec038fb43f3cd26684ce778ee0e80e81")
    version("1.48.0", commit="2bce60814db7c20949892587740fb484aa435978")
    version("1.46.1", commit="e422642f64815cdfee8fc340681ad87a7eafc3bb")
    version("1.42.0", commit="32baca734b599d60fa13bdbe31c5712e648f538d")
    version("1.36.1", commit="418e7e5647dd54d81b804455ddfcbc027fd0164a")
    version("1.34.0", commit="ebaad5ca61abb67c2c30c132e07531ba4257bccd")
    version("1.32.7", commit="4c56dc836dbfd0d228dc810e8d401811cdbc267c")
    version("1.30.3", commit="e99979054bc50ed8c0109bc54563036c1b368997")
    version("1.28.6", commit="197472d618f3ed04c795dc6ed435500c29619563")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.46.1:")
    depends_on("r-biocgenerics@0.21.2:", type=("build", "run"))
    depends_on("r-biocgenerics@0.25.3:", type=("build", "run"), when="@1.32.7:")
    depends_on("r-biocgenerics@0.37.0:", type=("build", "run"), when="@1.46.1:")
    depends_on("r-s4vectors@0.9.47:", type=("build", "run"))
    depends_on("r-s4vectors@0.17.32:", type=("build", "run"), when="@1.32.7:")
    depends_on("r-s4vectors@0.19.11:", type=("build", "run"), when="@1.34.0:")
    depends_on("r-s4vectors@0.27.12:", type=("build", "run"), when="@1.42.0:")
    depends_on("r-iranges@2.9.11:", type=("build", "run"))
    depends_on("r-iranges@2.11.16:", type=("build", "run"), when="@1.30.3:")
    depends_on("r-iranges@2.14.4:", type=("build", "run"), when="@1.32.7:")
    depends_on("r-iranges@2.15.12:", type=("build", "run"), when="@1.34.0:")
    depends_on("r-iranges@2.17.1:", type=("build", "run"), when="@1.36.1:")
    depends_on("r-iranges@2.23.9:", type=("build", "run"), when="@1.42.0:")
    depends_on("r-iranges@2.31.2:", type=("build", "run"), when="@1.50.1:")
    depends_on("r-genomeinfodb@1.11.5:", type=("build", "run"))
    depends_on("r-genomeinfodb@1.13.1:", type=("build", "run"), when="@1.30.3:")
    depends_on("r-genomeinfodb@1.15.2:", type=("build", "run"), when="@1.32.7:")
    depends_on("r-xvector", type=("build", "run"))
    depends_on("r-xvector@0.19.8:", type=("build", "run"), when="@1.32.7:")
    depends_on("r-xvector@0.29.2:", type=("build", "run"), when="@1.42.0:")
