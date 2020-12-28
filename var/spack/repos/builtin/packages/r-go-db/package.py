# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGoDb(RPackage):
    """A set of annotation maps describing the entire Gene
    Ontology assembled using data from GO."""

    homepage = "https://www.bioconductor.org/packages/GO.db/"
    url = "https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/GO.db_3.4.1.tar.gz"

    version('3.4.1', sha256='2fc2048e9d26edb98e35e4adc4d18c6df54f44836b5cc4a482d36ed99e058cc1')
    depends_on('r-annotationdbi', type=('build', 'run'))
