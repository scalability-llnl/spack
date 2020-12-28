# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGtrellis(RPackage):
    """Genome Level Trellis Layout.

       Genome level Trellis graph visualizes genomic data conditioned by
       genomic categories (e.g. chromosomes). For each genomic category,
       multiple dimensional data which are represented as tracks describe
       different features from different aspects. This package provides high
       flexibility to arrange genomic categories and to add self-defined
       graphics in the plot."""

    homepage = "https://bioconductor.org/packages/gtrellis"
    git      = "https://git.bioconductor.org/packages/gtrellis.git"

    version('1.16.1', commit='a9003ededc8f2a48c78d4545e2f214023c13a7da')
    version('1.14.0', commit='93935fb34211d12b250e22291712e18a31b0208d')
    version('1.12.1', commit='7f3941adddbbfa17f4cf474b703568678a38272d')
    version('1.11.1', commit='ff47d99743fd697d5c724f7bb18131dfe76dee71')
    version('1.8.0', commit='f813b420a008c459f63a2a13e5e64c5507c4c472')

    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-circlize@0.3.3:', type=('build', 'run'))
    depends_on('r-getoptlong', type=('build', 'run'))

    depends_on('r-circlize@0.4.8:', when='@1.16.1', type=('build', 'run'))
