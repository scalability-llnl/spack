# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenomeinfodbdata(RPackage):
    """for mapping between NCBI taxonomy ID and species. Used by functions
       in the GenomeInfoDb package."""

    homepage = "https://bioconductor.org/packages/GenomeInfoDbData/"
    url      = "https://bioconductor.org/packages/3.5/data/annotation/src/contrib/GenomeInfoDbData_0.99.0.tar.gz"

    version('1.2.1', sha256='75e6d683a29b8baeec66ba5194aa59a6aa69b04fae5a9c718a105c155fb41711',
            url='https://bioconductor.org/packages/3.9/data/annotation/src/contrib/GenomeInfoDbData_1.2.1.tar.gz')
    version('1.1.0', sha256='6efdca22839c90d455843bdab7c0ecb5d48e3b6c2f7b4882d3210a6bbad4304c',
            url='https://bioconductor.org/packages/3.7/data/annotation/src/contrib/GenomeInfoDbData_1.1.0.tar.gz')
    version('0.99.0', sha256='457049804bbd70f218c1c84067a23e83bdecb7304a3e4d8b697fee0b16dc1888')

    depends_on('r@3.3:', when='@0.99.0:1.1.0', type=('build', 'run'))
    depends_on('r@3.5:', when='@1.2.1:', type=('build', 'run'))
