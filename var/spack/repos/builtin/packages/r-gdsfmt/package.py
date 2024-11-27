# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGdsfmt(RPackage):
    """R Interface to CoreArray Genomic Data Structure (GDS) Files.

    This package provides a high-level R interface to CoreArray Genomic Data
    Structure (GDS) data files, which are portable across platforms with
    hierarchical structure to store multiple scalable array-oriented data
    sets with metadata information. It is suited for large-scale datasets,
    especially for data which are much larger than the available random-
    access memory. The gdsfmt package offers the efficient operations
    specifically designed for integers of less than 8 bits, since a diploid
    genotype, like single-nucleotide polymorphism (SNP), usually occupies
    fewer bits than a byte. Data compression and decompression are available
    with relatively efficient random access. It is also allowed to read a
    GDS file in parallel with multiple R processes supported by the package
    parallel."""

    bioc = "gdsfmt"

    license("BSD-2-Clause")

    version("1.36.0", commit="39ba0af93d499b0f9ef53f04d4f15e5436616f1a")
    version("1.34.0", commit="ab912c393d8eb6dc26f844a13422a29b9ce7265b")
    version("1.32.0", commit="06f2097cc10b1888739f86e635383a0f2ee7e208")
    version("1.30.0", commit="d27dde6a70bb2295f5bbc8961152b45ccee7a652")
    version("1.26.1", commit="bd180b21b1ace120035f0da255cbf6f13088f069")
    version("1.20.0", commit="b1fbaba0a5ace3dc45daecc85168651cd85dce00")
    version("1.18.1", commit="b911b953e9db7988e93ec2010b0ab1e384d073c9")
    version("1.16.0", commit="49b011452585e432b983b68466a230c9b71d8a95")
    version("1.14.1", commit="15743647b7eea5b82d3284858b4591fb6e59959d")
    version("1.12.0", commit="d705a95b0bea7be2a2b37e939f45017337ba0fb6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@2.15.0:", type=("build", "run"))
