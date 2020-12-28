# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKeggDb(RPackage):
    """A set of annotation maps for KEGG assembled using data from KEGG."""

    homepage = "https://www.bioconductor.org/packages/KEGG.db/"
    url = "https://www.bioconductor.org/packages/release/data/annotation/src/contrib/KEGG.db_3.2.3.tar.gz"

    version('3.2.3', sha256='02ea4630a3ec06a8d9a6151627c96d3f71dfc7e8857800bb5c0cdb6a838d6963')
    depends_on('r-annotationdbi', type=('build', 'run'))
