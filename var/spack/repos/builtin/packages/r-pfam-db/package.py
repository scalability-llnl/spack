# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPfamDb(RPackage):
    """A set of protein ID mappings for PFAM assembled using data from
    public repositories."""

    homepage = "https://www.bioconductor.org/packages/PFAM.db/"
    url      = "https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/PFAM.db_3.4.1.tar.gz"

    version('3.10.0', sha256='038888f95ce69230ac0e0b08aa3bcb09965682415520d437a7fb0a031eefe158')
    version('3.4.1', sha256='fc45a0d53139daf85873f67bd3f1b68f2d883617f4447caddbd2d7dcc58a393f')

    depends_on('r@2.7.0:', when='@3.4.1:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.37.4:', when='@3.4.1:', type=('build', 'run'))

    depends_on('r-annotationdbi@1.47.1:', when='@3.10.0:', type=('build', 'run'))
