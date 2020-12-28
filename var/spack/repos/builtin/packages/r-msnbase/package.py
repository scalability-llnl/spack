# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMsnbase(RPackage):
    """Base Functions and Classes for Mass Spectrometry and Proteomics.

       MSnbase provides infrastructure for manipulation, processing and
       visualisation of mass spectrometry and proteomics data, ranging from raw
       to quantitative and annotated data."""

    homepage = "https://bioconductor.org/packages/MSnbase"
    git      = "https://git.bioconductor.org/packages/MSnbase.git"

    version('2.10.1', commit='4d5899bc9c714f0b1a70cddd537cd4621b2b53b0')
    version('2.8.3', commit='ef883752c5e92d445647bc5b5d23d5df320db415')
    version('2.6.4', commit='46836860ce0281eef135303f2e2948303d67f68c')
    version('2.4.2', commit='c045d65daa730c7837852e6343a05cae9644ab5e')
    version('2.2.0', commit='d6e8fb7f106d05096fa9074da0f829ac8f02c197')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.7.1:', type=('build', 'run'))
    depends_on('r-biobase@2.15.2:', type=('build', 'run'))
    depends_on('r-mzr@2.7.6:', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-protgenerics@1.5.1:', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-vsn', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-impute', type=('build', 'run'))
    depends_on('r-pcamethods', type=('build', 'run'))
    depends_on('r-mzid@1.5.2:', type=('build', 'run'))
    depends_on('r-maldiquant@1.16:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))

    depends_on('r-mzr@2.11.11:', when='@2.4.2:', type=('build', 'run'))
    depends_on('r-protgenerics@1.9.1:', when='@2.4.2:', type=('build', 'run'))

    depends_on('r-mzr@2.13.6:', when='@2.6.4:', type=('build', 'run'))
    depends_on('r-iranges@2.13.28:', when='@2.6.4:', type=('build', 'run'))
    depends_on('r-scales', when='@2.6.4:', type=('build', 'run'))
    depends_on('r-mass', when='@2.6.4:', type=('build', 'run'))

    depends_on('r-mzr@2.15.1:', when='@2.8.3:', type=('build', 'run'))

    depends_on('r-mzr@2.17.3:', when='@2.10.1:', type=('build', 'run'))
