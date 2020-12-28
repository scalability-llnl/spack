# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRncl(RPackage):
    """rncl: An Interface to the Nexus Class Library.

    An interface to the Nexus Class Library which allows parsing of NEXUS,
    Newick and other phylogenetic tree file formats. It provides elements of
    the file that can be used to build phylogenetic objects such as ape's
    'phylo' or phylobase's 'phylo4(d)'. This functionality is demonstrated with
    'read_newick_phylo()' and 'read_nexus_phylo()'."""

    homepage = "https://github.com/fmichonneau/rncl"
    url      = "https://cloud.r-project.org/src/contrib/rncl_0.8.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rncl"

    version('0.8.4', sha256='6b19d0dd9bb08ecf99766be5ad684bcd1894d1cd9291230bdd709dbd3396496b')

    depends_on('r@3.1.1:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-progress@1.1.2:', type=('build', 'run'))
