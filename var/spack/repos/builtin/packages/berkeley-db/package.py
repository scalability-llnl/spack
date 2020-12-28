# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class BerkeleyDb(AutotoolsPackage):
    """Oracle Berkeley DB"""

    homepage = "https://www.oracle.com/database/technologies/related/berkeleydb.html"
    url      = "http://download.oracle.com/berkeley-db/db-18.1.40.tar.gz"

    version("18.1.40", sha256="0cecb2ef0c67b166de93732769abdeba0555086d51de1090df325e18ee8da9c8")
    version('18.1.32', sha256='fa1fe7de9ba91ad472c25d026f931802597c29f28ae951960685cde487c8d654')
    version('6.2.32', sha256='a9c5e2b004a5777aa03510cfe5cd766a4a3b777713406b02809c17c8e0e7a8fb')
    version('6.1.29', sha256='b3c18180e4160d97dd197ba1d37c19f6ea2ec91d31bbfaf8972d99ba097af17d')
    version('6.0.35', sha256='24421affa8ae436fe427ae4f5f2d1634da83d3d55a5ad6354a98eeedb825de55')
    version('5.3.28', sha256='e0a992d740709892e81f9d93f06daf305cf73fb81b545afe72478043172c3628')

    configure_directory = 'dist'
    build_directory = 'build_unix'

    def patch(self):
        # some of the docs are missing in 18.1.40
        if self.spec.satisfies("@18.1.40"):
            filter_file(r'bdb-sql', '', 'dist/Makefile.in')
            filter_file(r'gsg_db_server', '', 'dist/Makefile.in')

    def configure_args(self):
        config_args = [
            '--disable-static',
            '--enable-cxx',
            '--enable-dbm',
            '--enable-stl',
            # compat with system berkeley-db on darwin
            "--enable-compat185",
            # SSL support requires OpenSSL, but OpenSSL depends on Perl, which
            # depends on Berkey DB, creating a circular dependency
            '--with-repmgr-ssl=no',
        ]

        # The default glibc provided by CentOS 7 does not provide proper
        # atomic support when using the NVIDIA compilers
        if self.spec.satisfies('%nvhpc os=centos7'):
            config_args.append('--disable-atomicsupport')

        return config_args

    def test(self):
        """Perform smoke tests on the installed package binaries."""
        exes = [
            'db_checkpoint', 'db_deadlock', 'db_dump', 'db_load',
            'db_printlog', 'db_stat', 'db_upgrade', 'db_verify'
        ]
        for exe in exes:
            reason = 'test version of {0} is {1}'.format(exe,
                                                         self.spec.version)
            self.run_test(exe, ['-V'], [self.spec.version.string],
                          installed=True, purpose=reason, skip_missing=True)
