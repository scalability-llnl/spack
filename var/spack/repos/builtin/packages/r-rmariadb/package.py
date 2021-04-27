# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRmariadb(RPackage):
    """Database Interface and 'MariaDB' Driver

    Implements a 'DBI'-compliant interface to 'MariaDB'
    (<https://mariadb.org/>) and 'MySQL' (<https://www.mysql.com/>)
    databases."""

    homepage = "https://rmariadb.r-dbi.org/"
    url      = "https://cloud.r-project.org/src/contrib/RMariaDB_1.0.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RMariaDB"

    version('1.1.0', sha256='9ffa63a15052876a51a7996ca4e6a5b7b937f594b5cc7ca5a86f43789e22a956')
    version('1.0.8', sha256='3c8aedc519dc063ceb068535a3700bc5caf26f867078cc5a228aa8961e2d99f5')

    depends_on('r@2.8.0:', type=('build', 'run'))
    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-dbi@1.1.0:', type=('build', 'run'))
    depends_on('r-hms@0.5.0:', type=('build', 'run'))
    depends_on('r-lubridate', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.4:', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
    depends_on('r-plogr', type=('build', 'run'))
    depends_on('mariadb-client')

    patch('configure_add_rpath.patch')

    def configure_vars(self):
        lib_dir = self.spec['mariadb-client'].prefix.lib.mariadb
        inc_dir = self.spec['mariadb-client'].prefix.include.mariadb
        args = ['LIB_DIR={0}'.format(lib_dir),
                'INCLUDE_DIR={0}'.format(inc_dir)]
        return args
