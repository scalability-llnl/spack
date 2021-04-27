# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import architecture


class Sqlite(AutotoolsPackage):
    """SQLite3 is an SQL database engine in a C library. Programs that
       link the SQLite3 library can have SQL database access without
       running a separate RDBMS process.
    """
    homepage = "https://www.sqlite.org"

    version('3.35.4', sha256='7771525dff0185bfe9638ccce23faa0e1451757ddbda5a6c853bb80b923a512d')
    version('3.35.3', sha256='ecbccdd440bdf32c0e1bb3611d635239e3b5af268248d130d0445a32daf0274b')
    version('3.34.0', sha256='bf6db7fae37d51754737747aaaf413b4d6b3b5fbacd52bdb2d0d6e5b2edd9aee')
    version('3.33.0', sha256='106a2c48c7f75a298a7557bcc0d5f4f454e5b43811cc738b7ca294d6956bbb15')
    version('3.32.03', sha256='a31507123c1c2e3a210afec19525fd7b5bb1e19a6a34ae5b998fbd7302568b66')
    version('3.31.1', sha256='62284efebc05a76f909c580ffa5c008a7d22a1287285d68b7825a2b6b51949ae')
    version('3.30.1', sha256='8c5a50db089bd2a1b08dbc5b00d2027602ca7ff238ba7658fabca454d4298e60')
    version('3.30.0', sha256='e0a8cf4c7a87455e55e10413d16f358ca121ccec687fe1301eac95e2d340fc58')
    version('3.29.0', sha256='8e7c1e2950b5b04c5944a981cb31fffbf9d2ddda939d536838ebc854481afd5b')
    version('3.28.0', sha256='d61b5286f062adfce5125eaf544d495300656908e61fca143517afcc0a89b7c3')
    version('3.27.2', sha256='50c39e85ea28b5ecfdb3f9e860afe9ba606381e21836b2849efca6a0bfe6ef6e')
    version('3.27.1', sha256='54a92b8ff73ff6181f89b9b0c08949119b99e8cccef93dbef90e852a8b10f4f8')
    version('3.27.0', sha256='dbfb0fb4fc32569fa427d3658e888f5e3b84a0952f706ccab1fd7c62a54f10f0')
    version('3.26.0', sha256='5daa6a3fb7d1e8c767cd59c4ded8da6e4b00c61d3b466d0685e35c4dd6d7bf5d')
    # All versions prior to 3.26.0 are vulnerable to Magellan when FTS
    # is enabled, see https://blade.tencent.com/magellan/index_en.html

    depends_on('readline')
    depends_on('zlib')

    variant('functions', default=False,
            description='Provide mathematical and string extension functions '
                        'for SQL queries using the loadable extensions '
                        'mechanism.')

    variant('fts', default=True,
            description='Enable FTS support '
            '(unsafe for <3.26.0.0 due to Magellan).')

    variant('rtree', default=False, description='Build with Rtree module')
    variant('column_metadata', default=True, description="Build with COLUMN_METADATA")

    # See https://blade.tencent.com/magellan/index_en.html
    conflicts('+fts', when='@:3.25.99.99')

    resource(name='extension-functions',
             url='https://sqlite.org/contrib/download/extension-functions.c/download/extension-functions.c?get=25',
             sha256='991b40fe8b2799edc215f7260b890f14a833512c9d9896aa080891330ffe4052',
             expand=False,
             placement={'extension-functions.c?get=25':
                        'extension-functions.c'},
             when='+functions')

    # On some platforms (e.g., PPC) the include chain includes termios.h which
    # defines a macro B0. Sqlite has a shell.c source file that declares a
    # variable named B0 and will fail to compile when the macro is found. The
    # following patch undefines the macro in shell.c
    patch('sqlite_b0.patch', when='@3.18.0:3.21.0')

    # Starting version 3.17.0, SQLite uses compiler built-ins
    # __builtin_sub_overflow(), __builtin_add_overflow(), and
    # __builtin_mul_overflow(), which are not supported by Intel compiler.
    # Starting version 3.21.0 SQLite doesn't use the built-ins if Intel
    # compiler is used.
    patch('remove_overflow_builtins.patch', when='@3.17.0:3.20%intel')

    def url_for_version(self, version):
        full_version = list(version.version) + [0 * (4 - len(version.version))]
        version_string\
            = str(full_version[0]) + \
            ''.join(['%02d' % v for v in full_version[1:]])
        # See https://sqlite.org/chronology.html for version -> year
        # correspondence.
        if version >= Version('3.34.1'):
            year = '2021'
        elif version >= Version('3.31.0'):
            year = '2020'
        elif version >= Version('3.27.0'):
            year = '2019'
        elif version >= Version('3.22.0'):
            year = '2018'
        elif version >= Version('3.16.0'):
            year = '2017'
        elif version >= Version('3.10.0'):
            year = '2016'
        elif version >= Version('3.8.8'):
            year = '2015'
        elif version >= Version('3.8.3'):
            year = '2014'
        elif version >= Version('3.7.16'):
            year = '2013'
        else:
            raise ValueError('Unsupported version {0}'.format(version))
        return 'https://sqlite.org/{0}/sqlite-autoconf-{1}.tar.gz'.format(year, version_string)

    @property
    def libs(self):
        return find_libraries('libsqlite3', root=self.prefix.lib)

    def get_arch(self):
        arch = architecture.Arch()
        arch.platform = architecture.platform()
        return str(arch.platform.target('default_target'))

    def configure_args(self):
        args = []

        if self.get_arch() == 'ppc64le':
            args.append('--build=powerpc64le-redhat-linux-gnu')

        if '+fts' not in self.spec:
            args.extend(['--disable-fts4', '--disable-fts5'])

        # Ref: https://sqlite.org/rtree.html
        if '+rtree' in self.spec:
            args.append('CPPFLAGS=-DSQLITE_ENABLE_RTREE=1')

        # Ref: https://sqlite.org/compile.html
        if '+column_metadata' in self.spec:
            args.append('CPPFLAGS=-DSQLITE_ENABLE_COLUMN_METADATA=1')

        return args

    @run_after('install')
    def build_libsqlitefunctions(self):
        if '+functions' in self.spec:
            libraryname = 'libsqlitefunctions.' + dso_suffix
            cc = Executable(spack_cc)
            cc(self.compiler.cc_pic_flag, '-lm', '-shared',
                'extension-functions.c', '-o', libraryname)
            install(libraryname, self.prefix.lib)

    def _test_example(self):
        """Ensure a sequence of commands on example db are successful."""

        test_data_dir = self.test_suite.current_test_data_dir
        db_filename = test_data_dir.join('packages.db')
        exe = 'sqlite3'

        # Ensure the database only contains one table
        expected = 'packages'
        reason = 'test: ensuring only table is "{0}"'.format(expected)
        self.run_test(exe, [db_filename, '.tables'], expected, installed=True,
                      purpose=reason, skip_missing=False)

        # Ensure the database dump matches expectations, where special
        # characters are replaced with spaces in the expected and actual
        # output to avoid pattern errors.
        reason = 'test: checking dump output'
        expected = get_escaped_text_output(test_data_dir.join('dump.out'))
        self.run_test(exe, [db_filename, '.dump'], expected, installed=True,
                      purpose=reason, skip_missing=False)

    def _test_version(self):
        """Perform version check on the installed package."""
        exe = 'sqlite3'
        vers_str = str(self.spec.version)

        reason = 'test: ensuring version of {0} is {1}'.format(exe, vers_str)
        self.run_test(exe, '-version', vers_str, installed=True,
                      purpose=reason, skip_missing=False)

    def test(self):
        """Perform smoke tests on the installed package."""
        # Perform a simple version check
        self._test_version()

        # Run a sequence of operations
        self._test_example()
