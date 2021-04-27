# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RQtl(RPackage):
    """Tools for Analyzing QTL Experiments

    Analysis of experimental crosses to identify genes (called quantitative
    trait loci, QTLs) contributing to variation in quantitative traits. Broman
    et al. (2003) <doi:10.1093/bioinformatics/btg112>."""

    homepage = "http://rqtl.org"
    url      = "https://cloud.r-project.org/src/contrib/qtl_1.44-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/qtl"

    version('1.47-9', sha256='6ba4e7b40d946b3ab68d54624599284b1d352c86fb50d31b134826be758ece41')
    version('1.44-9', sha256='315063f0c3fbb95cd2169eb4109ade0339e8f3c28670b38c3167214b9bdf950e')

    depends_on('r@2.14.0:', type=('build', 'run'))
