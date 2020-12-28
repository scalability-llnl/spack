# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQtl(RPackage):
    """qtl: Tools for Analyzing QTL Experiments"""

    homepage = "http://rqtl.org"
    url      = "https://cloud.r-project.org/src/contrib/qtl_1.44-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/qtl"

    version('1.44-9', sha256='315063f0c3fbb95cd2169eb4109ade0339e8f3c28670b38c3167214b9bdf950e')

    depends_on('r@2.14.0:', type=('build', 'run'))
