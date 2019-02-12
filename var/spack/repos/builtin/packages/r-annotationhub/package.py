# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnnotationhub(RPackage):
    """This package provides a client for the Bioconductor AnnotationHub web
       resource. The AnnotationHub web resource provides a central location
       where genomic files (e.g., VCF, bed, wig) and other resources from
       standard locations (e.g., UCSC, Ensembl) can be discovered. The
       resource includes metadata about each resource, e.g., a textual
       description, tags, and date of modification. The client creates and
       manages a local cache of files retrieved by the user, helping with
       quick and reproducible access."""

    homepage = "https://bioconductor.org/packages/AnnotationHub/"
    git      = "https://git.bioconductor.org/packages/AnnotationHub.git"

    version('2.8.3', commit='8aa9c64262a8d708d2bf1c82f82dfc3d7d4ccc0c')

    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-biocinstaller', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-interactivedisplaybase', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.8.3')
