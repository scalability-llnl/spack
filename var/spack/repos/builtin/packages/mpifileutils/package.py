# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Mpifileutils(DynamicInheritancePackage):
    """mpiFileUtils is a suite of MPI-based tools to manage large datasets,
       which may vary from large directory trees to large files.
       High-performance computing users often generate large datasets with
       parallel applications that run with many processes (millions in some
       cases). However those users are then stuck with single-process tools
       like cp and rm to manage their datasets. This suite provides
       MPI-based tools to handle typical jobs like copy, remove, and compare
       for such datasets, providing speedups of up to 20-30x."""

    homepage = "https://github.com/hpc/mpifileutils"
    url      = "https://github.com/hpc/mpifileutils/releases/download/v0.6/mpifileutils-0.6.tar.gz"
    git      = "https://github.com/hpc/mpifileutils.git"

    version('develop', branch='master')
    version('0.8.1', 'acbd5b5c15919a67392509614bb7871e')
    version('0.8', '1082600e7ac4e6b2c13d91bbec40cffb')
    version('0.7', 'c081f7f72c4521dddccdcf9e087c5a2b')
    version('0.6', '620bcc4966907481f1b1a965b28fc9bf')

    classes = {
        AutotoolsPackage: '@:0.8.1',
        CMakePackage: '@0.9:'
    }

    conflicts('platform=darwin')

    depends_on('mpi')
    depends_on('libcircle')
    depends_on('lwgrp')

    # need precise version of dtcmp, since DTCMP_Segmented_exscan added
    # in v1.0.3 but renamed in v1.1.0 and later
    depends_on('dtcmp@1.0.3',  when='@:0.7')
    depends_on('dtcmp@1.1.0:', when='@0.8:')

    depends_on('libarchive')

    depends_on('cmake@3.1:', when='@0.9:', type='build')

    variant('build_type', default='RelWithDebInfo',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    variant('xattr', default=True,
        description="Enable code for extended attributes")

    variant('lustre', default=False,
        description="Enable optimizations and features for Lustre")

    variant('gpfs', default=False,
        description="Enable optimizations and features for GPFS")
    # gpfs support added after v0.8.1
    conflicts('+gpfs', when='@:0.8.1')

    variant('experimental', default=False,
        description="Install experimental tools")
    # --enable-experimental fails with v0.6 and earlier
    conflicts('+experimental', when='@:0.6')

    # return code bug in older versions prevents building with clang
    conflicts('%clang', when='@:0.8.1')

    # autotools versions do not implement MinSizeRel build type
    conflicts('build_type=MinSizeRel', when='@:0.8.1')

    def flag_handler(self, name, flags):
        if name == 'cflags' and self.spec.satisfies('@:0.8.1'):
            # handle cmake-style variant for pre-cmake versions
            build_type = self.spec.variants['build_type'].value
            if build_type in ('Debug', 'RelWithDebInfo'):
                flags.append('-g')
            elif build_type in ('Release', 'RelWithDebInfo'):
                flags.append('-O2')
        return (flags, None, None)

    # 0.9 and later are cmake packages. Use these cmake args
    def cmake_args(self):
        args = []
        args.append("-DWITH_DTCMP_PREFIX=%s" % self.spec['dtcmp'].prefix)
        args.append("-DWITH_LibCircle_PREFIX=%s" %
                    self.spec['libcircle'].prefix)

        if '+xattr' in self.spec:
            args.append("-DENABLE_XATTRS=ON")
        else:
            args.append("-DENABLE_XATTRS=OFF")

        if '+lustre' in self.spec:
            args.append("-DENABLE_LUSTRE=ON")
        else:
            args.append("-DENABLE_LUSTRE=OFF")

        if '+gpfs' in self.spec:
            args.append("-DENABLE_GPFS=ON")
        else:
            args.append("-DENABLE_GPFS=OFF")

        if '+experimental' in self.spec:
            args.append("-DENABLE_EXPERIMENTAL=ON")
        else:
            args.append("-DENABLE_EXPERIMENTAL=OFF")

        return args

    # 0.8.1 and earlier are autotools build. use these configure args
    def configure_args(self):
        args = []
        args.append("CPPFLAGS=-I%s/src/common" % pwd())
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

        if '+xattr' in self.spec:
            args.append('CFLAGS=-DDCOPY_USE_XATTRS')

        if '+lustre' in self.spec:
            args.append('--enable-lustre')
        else:
            args.append('--disable-lustre')

        # does this propagate forward, for <=0.7?
        if self.spec.satisfies('@0.7:'):
            if '+experimental' in self.spec:
                args.append('--enable-experimental')
            else:
                args.append('--disable-experimental')

        return args
