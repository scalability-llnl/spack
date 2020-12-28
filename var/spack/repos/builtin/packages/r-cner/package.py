# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCner(RPackage):
    """CNE Detection and Visualization.

       Large-scale identification and advanced visualization of sets of
       conserved noncoding elements."""

    homepage = "https://bioconductor.org/packages/CNEr"
    git      = "https://git.bioconductor.org/packages/CNEr.git"

    version('1.20.0', commit='9c25d8e8f6f5fd8a5311f554c86e7ca1140a4ca5')
    version('1.18.1', commit='66aa88af04364c81832f3b09bad898f3c117f606')
    version('1.16.1', commit='a2bec4b98d5938709f959a69c151f553ef357941')
    version('1.14.0', commit='b8634d65c51728c815127e22b45eba7c9b9db897')
    version('1.12.1', commit='90d611f9cd19a73d0fe92ab03ef428519d64c017')

    depends_on('r@3.2.2:', type=('build', 'run'))
    depends_on('r-biostrings@2.33.4:', type=('build', 'run'))
    depends_on('r-rsqlite@0.11.4:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.1.3:', type=('build', 'run'))
    depends_on('r-genomicranges@1.23.16:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.25.5:', type=('build', 'run'))
    depends_on('r-xvector@0.5.4:', type=('build', 'run'))
    depends_on('r-genomicalignments@1.1.9:', type=('build', 'run'))
    depends_on('r-dbi@0.6:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', type=('build', 'run'))
    depends_on('r-iranges@2.5.27:', type=('build', 'run'))
    depends_on('r-readr@0.2.2:', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-reshape2@1.4.1:', type=('build', 'run'))
    depends_on('r-ggplot2@2.1.0:', type=('build', 'run'))
    depends_on('r-powerlaw@0.60.3:', type=('build', 'run'))
    depends_on('r-annotate@1.50.0:', type=('build', 'run'))
    depends_on('r-go-db@3.3.0:', type=('build', 'run'))
    depends_on('r-r-utils@2.3.0:', type=('build', 'run'))
    depends_on('r-keggrest@1.14.0:', type=('build', 'run'))

    depends_on('r@3.4:', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-dbi@0.7:', when='@1.14.0:', type=('build', 'run'))
