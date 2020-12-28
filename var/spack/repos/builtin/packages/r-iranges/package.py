# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIranges(RPackage):
    """Foundation of integer range manipulation in Bioconductor.

       Provides efficient low-level and highly reusable S4 classes for storing,
       manipulating and aggregating over annotated ranges of integers.
       Implements an algebra of range operations, including efficient
       algorithms for finding overlaps and nearest neighbors. Defines efficient
       list-like classes for storing, transforming and aggregating large
       grouped data, i.e., collections of atomic vectors and DataFrames."""

    homepage = "https://bioconductor.org/packages/IRanges"
    git      = "https://git.bioconductor.org/packages/IRanges.git"

    version('2.22.2', commit='8c5e991')
    version('2.18.3', commit='c98a7ba074e72f2e5ec98252dffe9d3392711972')
    version('2.16.0', commit='26834c6868d7c279dd8ac1bb9daa16e6fef273c2')
    version('2.14.12', commit='00af02756c14771a23df9efcf379409ab6eb3041')
    version('2.12.0', commit='1b1748655a8529ba87ad0f223f035ef0c08e7fcd')
    version('2.10.5', commit='b00d1d5025e3c480d17c13100f0da5a0132b1614')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.21.1:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.17:', type=('build', 'run'))

    depends_on('r-biocgenerics@0.23.3:', when='@2.12.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.15.5:', when='@2.12.0:', type=('build', 'run'))

    depends_on('r-biocgenerics@0.25.3:', when='@2.14.12:', type=('build', 'run'))
    depends_on('r-s4vectors@0.18.2:', when='@2.14.12:', type=('build', 'run'))

    depends_on('r-s4vectors@0.19.11:', when='@2.16.0:', type=('build', 'run'))

    depends_on('r-s4vectors@0.21.9:', when='@2.18.3:', type=('build', 'run'))

    depends_on('r-s4vectors@0.25.14:', when='@2.22.2:', type=('build', 'run'))
