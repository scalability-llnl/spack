# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPegas(RPackage):
    """Population and Evolutionary Genetics Analysis System

    Functions for reading, writing, plotting, analysing, and
    manipulating allelic and haplotypic data, including from VCF files,
    and for the analysis of population nucleotide sequences and
    micro-satellites including coalescent analyses, linkage
    disequilibrium, population structure (Fst, Amova) and equilibrium
    (HWE), haplotype networks, minimum spanning tree and network, and
    median-joining networks."""

    homepage = "http://ape-package.ird.fr/pegas.html"
    url      = "https://cloud.r-project.org/src/contrib/pegas_0.14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pegas"

    maintainers = ['dorton21']

    version('0.14', sha256='7df90e6c4a69e8dbed2b3f68b18f1975182475bf6f86d4159256b52fd5332053')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-ape@5.3-11:', type=('build', 'run'))
    depends_on('r-adegenet', type=('build', 'run'))
