# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRpostgres(RPackage):
    """'Rcpp' Interface to 'PostgreSQL'

    Fully 'DBI'-compliant 'Rcpp'-backed interface to 'PostgreSQL'
    <https://www.postgresql.org/>, an open-source relational database."""

    homepage = "https://rpostgres.r-dbi.org/"
    cran     = "RPostgres"

    version('1.3.1', sha256='f68ab095567317ec32d3faa10e5bcac400aee5aeca8d7132260d4e90f82158ea')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-blob@1.2.0:', type=('build', 'run'))
    depends_on('r-dbi@1.1.0:', type=('build', 'run'))
    depends_on('r-hms@0.5.0:', type=('build', 'run'))
    depends_on('r-lubridate', type=('build', 'run'))
    depends_on('r-rcpp@0.11.4.2:', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
    depends_on('r-plogr@0.2.0:', type=('build', 'run'))
    depends_on('postgresql@9.0:', type=('build', 'run'))

    # The postgresql pkg-config file does not contain rpath flags. This recipe
    # passes LIB_DIR and INCLUDE_DIR instead of using pkg-config. The below
    # patch ensures that the rpath flags are added in that case.
    patch('configure_add_rpath.patch')

    def configure_vars(self):
        lib_dir = self.spec['postgresql'].prefix.lib
        inc_dir = self.spec['postgresql'].prefix.include
        args = ['LIB_DIR={0}'.format(lib_dir),
                'INCLUDE_DIR={0}'.format(inc_dir)]
        return args
