# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiomart(RPackage):
    """Interface to BioMart databases (i.e. Ensembl).

       In recent years a wealth of biological data has become available in
       public data repositories. Easy access to these valuable data resources
       and firm integration with data analysis is needed for comprehensive
       bioinformatics data analysis. biomaRt provides an interface to a growing
       collection of databases implementing the BioMart software suite
       (<http://www.biomart.org>). The package enables retrieval of large
       amounts of data in a uniform way without the need to know the underlying
       database schemas or write complex SQL queries. The most prominent
       examples of BioMart databases are maintain by Ensembl, which provides
       biomaRt users direct access to a diverse set of data and enables a wide
       range of powerful online queries from gene annotation to database
       mining."""

    homepage = "https://bioconductor.org/packages/biomaRt"
    git      = "https://git.bioconductor.org/packages/biomaRt.git"

    version('2.40.5', commit='ed9ddafb0d620168ea8e3ab4884f3457b8525c68')
    version('2.38.0', commit='16b997aba19a90a1c5fa64c442b1e7fcff99a658')
    version('2.36.1', commit='5634e57e20199f9dc1f8b927eb3893143fc02f4f')
    version('2.34.2', commit='a7030915fbc6120cc6812aefdedba423a207459b')
    version('2.32.1', commit='f84d74424fa599f6d08f8db4612ca09914a9087f')

    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))

    depends_on('r-progress', when='@2.34.2:', type=('build', 'run'))
    depends_on('r-stringr', when='@2.34.2:', type=('build', 'run'))
    depends_on('r-httr', when='@2.34.2:', type=('build', 'run'))
