# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RWaldo(RPackage):
    """Find Differences Between R Objects

    Compare complex R objects and reveal the key differences. Designed
    particularly for use in testing packages where being able to quickly
    isolate key differences makes understanding test failures much easier."""

    homepage = "https://github.com/r-lib/waldo"
    url      = "https://cloud.r-project.org/src/contrib/waldo_0.2.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/waldo"

    version('0.2.3', sha256='1fbab22fe9be6ca8caa3df7306c763d7025d81ab6f17b85daaf8bdc8c9455c53')

    depends_on('r-cli', type=('build', 'run'))
    depends_on('r-diffobj', type=('build', 'run'))
    depends_on('r-fansi', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-rematch2', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
