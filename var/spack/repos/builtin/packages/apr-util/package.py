# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AprUtil(AutotoolsPackage):
    """Apache Portable Runtime Utility"""

    homepage  = 'https://apr.apache.org/'
    url       = 'https://archive.apache.org/dist/apr/apr-util-1.6.1.tar.gz'

    version('1.6.1', sha256='b65e40713da57d004123b6319828be7f1273fbc6490e145874ee1177e112c459')
    version('1.6.0', sha256='483ef4d59e6ac9a36c7d3fd87ad7b9db7ad8ae29c06b9dd8ff22dda1cc416389')
    version('1.5.4', sha256='976a12a59bc286d634a21d7be0841cc74289ea9077aa1af46be19d1a6e844c19')

    variant('crypto', default=True,  description='Enable crypto support')
    variant('gdbm',   default=False, description='Enable GDBM support')
    variant('pgsql',  default=False, description='Enable PostgreSQL support')
    variant('sqlite', default=False, description='Enable sqlite DBD driver')
    variant('odbc',   default=False, description='Enalbe ODBC support')

    depends_on('apr')
    depends_on('expat')
    depends_on('iconv')

    depends_on('openssl', when='+crypto')
    depends_on('gdbm', when='+gdbm')
    depends_on('postgresql', when='+pgsql')
    depends_on('sqlite', when='+sqlite')
    depends_on('unixodbc', when='+odbc')

    def configure_args(self):
        spec = self.spec

        args = [
            '--with-apr={0}'.format(spec['apr'].prefix),
            '--with-expat={0}'.format(spec['expat'].prefix),
            '--with-iconv={0}'.format(spec['iconv'].prefix),
            # TODO: Add support for the following database managers
            '--without-ndbm',
            '--without-berkeley-db',
            '--without-mysql',
            '--without-oracle',
        ]

        if '+crypto' in spec:
            args.extend([
                '--with-crypto',
                '--with-openssl={0}'.format(spec['openssl'].prefix),
            ])
        else:
            args.append('--without-crypto')

        if '+gdbm' in spec:
            args.append('--with-gdbm={0}'.format(spec['gdbm'].prefix))
        else:
            args.append('--without-gdbm')

        if '+pgsql' in spec:
            args.append('--with-pgsql={0}'.format(spec['postgresql'].prefix))
        else:
            args.append('--without-pgsql')

        if '+sqlite' in spec:
            if spec.satisfies('^sqlite@3.0:3.999'):
                args.extend([
                    '--with-sqlite3={0}'.format(spec['sqlite'].prefix),
                    '--without-sqlite2',
                ])
            elif spec.satisfies('^sqlite@2.0:2.999'):
                args.extend([
                    '--with-sqlite2={0}'.format(spec['sqlite'].prefix),
                    '--without-sqlite3',
                ])
        else:
            args.extend([
                '--without-sqlite2',
                '--without-sqlite3',
            ])

        if '+odbc' in spec:
            args.append('--with-odbc={0}'.format(spec['unixodbc'].prefix))
        else:
            args.append('--without-odbc')

        return args

    def check(self):
        # FIXME: Database driver tests fail, at least on macOS:
        #
        # Failed to load driver file apr_dbd_pgsql.so
        # Failed to load driver file apr_dbd_sqlite3.so
        # Failed to load driver file apr_dbd_odbc.so

        # Tests occassionally fail when run in parallel
        make('check', parallel=False)
