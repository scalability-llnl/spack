# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnnotationhub(RPackage):
    """Client to access AnnotationHub resources.

       This package provides a client for the Bioconductor AnnotationHub web
       resource. The AnnotationHub web resource provides a central location
       where genomic files (e.g., VCF, bed, wig) and other resources from
       standard locations (e.g., UCSC, Ensembl) can be discovered. The resource
       includes metadata about each resource, e.g., a textual description,
       tags, and date of modification. The client creates and manages a local
       cache of files retrieved by the user, helping with quick and
       reproducible access."""

    homepage = "https://bioconductor.org/packages/AnnotationHub"
    git      = "https://git.bioconductor.org/packages/AnnotationHub.git"

    version('2.16.1', commit='f8cefaae603b782e1c1ad277a3fb89d44e3aa1ed')
    version('2.14.5', commit='993a98ce3de04a0bbddcbde5b1ab2a9550275a12')
    version('2.12.1', commit='471407bd9cdc612e01deb071c91bd9e5f1ea5e55')
    version('2.10.1', commit='b7cb668de9b9625ac2beb3dcde1fa39e289eec29')
    version('2.8.3', commit='8aa9c64262a8d708d2bf1c82f82dfc3d7d4ccc0c')

    depends_on('r-biocgenerics@0.15.10:', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-biocinstaller', type=('build', 'run'))
    depends_on('r-annotationdbi@1.31.19:', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-interactivedisplaybase', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))

    depends_on('r-curl', when='@2.10.1:', type=('build', 'run'))

    depends_on('r-biocmanager', when='@2.14.5:', type=('build', 'run'))

    depends_on('r-biocfilecache@1.5.1:', when='@2.16.1:', type=('build', 'run'))
    depends_on('r-rappdirs', when='@2.16.1:', type=('build', 'run'))
    depends_on('r-dplyr', when='@2.16.1:', type=('build', 'run'))
