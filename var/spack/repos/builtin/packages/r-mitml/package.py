# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMitml(RPackage):
    """Provides tools for multiple imputation of missing data in multilevel
    modeling. Includes a user-friendly interface to the packages 'pan' and
    'jomo', and several functions for visualization, data management and the
    analysis of multiply imputed data sets."""

    homepage = "https://cloud.r-project.org/package=mitml"
    url      = "https://cloud.r-project.org/src/contrib/mitml_0.3-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mitml"

    version('0.3-7', sha256='c6f796d0059f1b093b599a89d955982fa257de9c45763ecc2cbbce10fdec1e7b')
    version('0.3-6', sha256='bc59bdc802eb882340393752535446560c716f12c6fca2b95f03c6af30d978de')
    version('0.3-5', sha256='8bcfeb18f3fb8a58a516348c37369eb8356af4bd3e0688c84a2366e1534608e9')

    depends_on('r-pan', type=('build', 'run'))
    depends_on('r-jomo', type=('build', 'run'))
    depends_on('r-haven', type=('build', 'run'))
