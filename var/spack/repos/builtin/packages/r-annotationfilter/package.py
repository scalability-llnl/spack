# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnnotationfilter(RPackage):
    """Facilities for Filtering Bioconductor Annotation Resources.

       This package provides class and other infrastructure to implement
       filters for manipulating Bioconductor annotation resources. The filters
       will be used by ensembldb, Organism.dplyr, and other packages."""

    homepage = "https://bioconductor.org/packages/AnnotationFilter"
    git      = "https://git.bioconductor.org/packages/AnnotationFilter.git"

    version('1.8.0', commit='9bf70ead899e32e84e2908f2b29cd38250d2d1ed')
    version('1.6.0', commit='fa40a7e17e93fac9e85091ff93f256adf145dec3')
    version('1.4.0', commit='acbd3309f478843a7899bd9773af5f19f986b829')
    version('1.2.0', commit='744b82915d7b85031de462d9d0a2bf9fdfd0e29d')
    version('1.0.0', commit='a9f79b26defe3021eea60abe16ce1fa379813ec9')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
