# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmariadb(RPackage):
    """Implements a 'DBI'-compliant interface to 'MariaDB'
    (<https://mariadb.org/>) and 'MySQL' (<https://www.mysql.com/>)
    databases."""

    homepage = "https://rmariadb.r-dbi.org/"
    url      = "https://cloud.r-project.org/src/contrib/RMariaDB_1.0.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RMariaDB"

    version('1.0.8', sha256='3c8aedc519dc063ceb068535a3700bc5caf26f867078cc5a228aa8961e2d99f5')

    depends_on('r@2.8.0:', type=('build', 'run'))
    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-dbi@1.1.0:', type=('build', 'run'))
    depends_on('r-hms@0.5.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.4:', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
    depends_on('r-plogr', type=('build', 'run'))

    # non-R dependencies
    depends_on('mariadb-client')
