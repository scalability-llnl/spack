# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REcp(RPackage):
    """ecp: Non-Parametric Multiple Change-Point Analysis of
       MultivariateData"""

    homepage = "https://cloud.r-project.org/package=ecp"
    url      = "https://cloud.r-project.org/src/contrib/ecp_3.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ecp"

    version('3.1.1', sha256='d2ab194e22e6ab0168222fbccfcf2e25c6cd51a73edc959086b0c6e0a7410268')

    depends_on('r@3.00:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
