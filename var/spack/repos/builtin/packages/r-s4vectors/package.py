# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RS4vectors(RPackage):
    """Foundation of vector-like and list-like containers in Bioconductor.

       The S4Vectors package defines the Vector and List virtual classes and a
       set of generic functions that extend the semantic of ordinary vectors
       and lists in R. Package developers can easily implement vector-like or
       list-like objects as concrete subclasses of Vector or List. In addition,
       a few low-level concrete subclasses of general interest (e.g. DataFrame,
       Rle, and Hits) are implemented in the S4Vectors package itself (many
       more are implemented in the IRanges package and in other Bioconductor
       infrastructure packages)."""

    homepage = "https://bioconductor.org/packages/S4Vectors"
    git      = "https://git.bioconductor.org/packages/S4Vectors.git"

    version('0.26.1', commit='935769c')
    version('0.22.1', commit='d25e517b48ca4184a4c2ee1f8223c148a55a8b8a')
    version('0.20.1', commit='1878b2909086941e556c5ea953c6fd86aebe9b02')
    version('0.18.3', commit='d6804f94ad3663828440914920ac933b934aeff1')
    version('0.16.0', commit='00fec03fcbcb7cff37917fab0da28d91fdf9dc3d')
    version('0.14.7', commit='40af17fe0b8e93b6a72fc787540d2961773b8e23')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.21.1:', type=('build', 'run'))

    depends_on('r-biocgenerics@0.23.3:', when='@0.16.0:0.22.1', type=('build', 'run'))
    depends_on('r-biocgenerics@0.31.1:', when='@0.26.1:', type=('build', 'run'))
