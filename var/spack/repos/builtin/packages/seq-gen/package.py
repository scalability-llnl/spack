# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SeqGen(MakefilePackage):
    """Seq-Gen is a program that will simulate the evolution of nucleotide or
    amino acid sequences along a phylogeny.

    Seq-Gen is a program that will simulate the evolution of nucleotide or
    amino acid sequences along a phylogeny, using common models of the
    substitution process. A range of models of molecular evolution are implemented
    including the general reversible model. State frequencies and other parameters
    of the model may be given and site-specific rate heterogeneity may also be
    incorporated in a number of ways. Any number of trees may be read in and the
    program will produce any number of data sets for each tree. Thus large sets of
    replicate simulations can be easily created. It has been designed to be a
    general purpose simulator that incorporates most of the commonly used (and
    computationally tractable) models of molecular sequence evolution."""

    homepage = "http://tree.bio.ed.ac.uk/software/Seq-Gen/"
    url = "https://github.com/rambaut/Seq-Gen/archive/refs/tags/1.3.4.tar.gz"

    version("1.3.4", sha256="092ec2255ce656a02b2c3012c32443c7d8e38c692f165fb155b304ca030cbb59")

    depends_on("c", type="build")  # generated

    build_directory = "source"

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("source/seq-gen", prefix.bin)
