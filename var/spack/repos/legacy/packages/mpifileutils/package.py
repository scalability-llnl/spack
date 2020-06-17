# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Mpifileutils(AutotoolsPackage):
    """mpiFileUtils is a suite of MPI-based tools to manage large datasets,
    which may vary from large directory trees to large files.

    High-performance computing users often generate large datasets with
    parallel applications that run with many processes (millions in some
    cases). However those users are then stuck with single-process tools
    like cp and rm to manage their datasets. This suite provides
    MPI-based tools to handle typical jobs like copy, remove, and compare
    for such datasets, providing speedups of up to 20-30x.
    """

    homepage = "https://github.com/hpc/mpifileutils"
    url = "https://github.com/hpc/mpifileutils/archive/v0.9.tar.gz"
    git = "https://github.com/hpc/mpifileutils.git"

    version('0.8.1', sha256='7181fc47d985d858dcc24f2767649ed5c476d3b1f2e6846e1b494869d36da7d7')
    version('0.8',   sha256='325442d5ed0114b5721f01a677992f9f99e552acc28948ff9b78ad000b097ccb')
    version('0.7',   sha256='74cc36c9310dc266b16fe8de1f6855b440935a42ff5cc36585344ff9a3588973')
    version('0.6',   sha256='1f7ddc6f1b73c8b0d00d3021a1228d786cacc326f76486b38ec9edeb53d1d68b')

    conflicts('platform=darwin')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    depends_on('mpi')
    depends_on('libcircle@0.3:')

    # need precise version of dtcmp, since DTCMP_Segmented_exscan added
    # in v1.0.3 but renamed in v1.1.0 and later
    depends_on('dtcmp@1.0.3',  when='@:0.7')
    depends_on('dtcmp@1.1.0:', when='@0.8:')

    depends_on('libarchive')

    variant('xattr', default=True,
            description="Enable code for extended attributes")

    variant('lustre', default=False,
            description="Enable optimizations and features for Lustre")

    variant('experimental', default=False,
            description="Install experimental tools")
    conflicts('+experimental', when='@:0.6')

    def configure_args(self):
        args = [
            'LDFLAGS=-L{0}'.format(self.spec['dtcmp'].prefix.lib)
        ]

        if '+xattr' in self.spec:
            args.append('CFLAGS=-DDCOPY_USE_XATTRS')

        args.append("libarchive_CFLAGS=-I%s"
                    % self.spec['libarchive'].prefix.include)
        args.append("libarchive_LIBS=%s %s"
                    % (self.spec['libarchive'].libs.search_flags,
                       self.spec['libarchive'].libs.link_flags))
        args.append("libcircle_CFLAGS=-I%s"
                    % self.spec['libcircle'].prefix.include)
        args.append("libcircle_LIBS=%s %s"
                    % (self.spec['libcircle'].libs.search_flags,
                       self.spec['libcircle'].libs.link_flags))
        args.append("--with-dtcmp=%s" % self.spec['dtcmp'].prefix)
        args.extend(self.enable_or_disable('lustre'))

        if self.spec.satisfies('@0.7:'):
            args.extend(self.enable_or_disable('experimental'))

        return args
