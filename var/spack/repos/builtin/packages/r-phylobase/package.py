# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhylobase(RPackage):
    """phylobase: Base Package for Phylogenetic Structures and Comparative
    Data.

    Provides a base S4 class for comparative methods, incorporating one or
    more trees and trait data."""

    homepage = "https://github.com/fmichonneau/phylobase"
    url      = "https://cloud.r-project.org/src/contrib/phylobase_0.8.10.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/phylobase"

    version('0.8.10', sha256='5a44380ff49bab333a56f6f96157324ade8afb4af0730e013194c4badb0bf94b')

    depends_on('r-ade4', type=('build', 'run'))
    depends_on('r-ape@3.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-rncl@0.6.0:', type=('build', 'run'))
    depends_on('r-rnexml', type=('build', 'run'))
