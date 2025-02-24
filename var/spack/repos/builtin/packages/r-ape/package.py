# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RApe(RPackage):
    """Analyses of Phylogenetics and Evolution.

    Functions for reading, writing, plotting, and manipulating phylogenetic
    trees, analyses of comparative data in a phylogenetic framework, ancestral
    character analyses, analyses of diversification and macroevolution,
    computing distances from DNA sequences, reading and writing nucleotide
    sequences as well as importing from BioConductor, and several tools such as
    Mantel's test, generalized skyline plots, graphical exploration of
    phylogenetic data (alex, trex, kronoviz), estimation of absolute
    evolutionary rates and clock-like trees using mean path lengths and
    penalized likelihood, dating trees with non-contemporaneous sequences,
    translating DNA into AA sequences, and assessing sequence alignments.
    Phylogeny estimation can be done with the NJ, BIONJ, ME, MVR, SDM, and
    triangle methods, and several methods handling incomplete distance matrices
    (NJ*, BIONJ*, MVR*, and the corresponding triangle method). Some functions
    call external applications (PhyML, Clustal, T-Coffee, Muscle) whose results
    are returned into R."""

    cran = "ape"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("5.8", sha256="24ce729979e1bcc60317e71e5100ce54156ceb7484917b0d64260f733ae84d24")
    version("5.7-1", sha256="8b09c71218d8aa629e43bc807b433a4e30a61847d91b2810e31c366f0fe5057a")
    version("5.6-2", sha256="9b62450a0390a1f07df007d348ad4cedcd814d42cb11c5a300ed33550fd41257")
    version("5.6-1", sha256="25401e036576eed1200e15bf68879ccd85611303a3508b989e15164cd4c0f7f7")
    version("5.4-1", sha256="f0316c8e74ce900053e8b3e8c9322b9d10e7730f3be2150365f74630bee7eee4")
    version("5.3", sha256="08b0df134c523feb00a86896d1aa2a43f0f0dab20a53bc6b5d6268d867988b23")
    version("5.2", sha256="27eb02856c130d59de6e06276be4981709923756319e465a7f2d4756d4f46415")
    version("5.1", sha256="b7d5dca66881638227a40aa59533904aa5efe0f4b867851b248e8f948a01a26e")
    version("5.0", sha256="c32ed22e350b3d7c7ef3de9334155ab1f3086922b5ec9a1643897cae7abda960")
    version("4.1", sha256="935af5ddadcba832d3f9cc032a80fc1a2e627a7ed54ef5f3773f87e06374a924")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@5.7-1:")
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-rcpp@0.12.0:", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"), when="@5.7-1:")
