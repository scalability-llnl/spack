# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFitModels(RPackage):
    """Compare Fitted Models"""

    homepage = "https://cloud.r-project.org/package=fit.models"
    url      = "https://cloud.r-project.org/src/contrib/fit.models_0.5-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fit.models"

    version('0.5-14', sha256='93b9d119e97b36c648a19c891fc5e69f5306eb5b9bac16bf377555057afd4b6e')
    version('0.5-13', sha256='7df545fce135159e9abf0a19076628d3ec2999e89f018e142a7a970428823d48')

    depends_on('r-lattice', type=('build', 'run'))
