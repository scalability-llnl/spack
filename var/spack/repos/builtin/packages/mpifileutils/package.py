# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpifileutils(Package):
    """mpiFileUtils is a suite of MPI-based tools to manage large datasets,
       which may vary from large directory trees to large files.
       High-performance computing users often generate large datasets with
       parallel applications that run with many processes (millions in some
       cases). However those users are then stuck with single-process tools
       like cp and rm to manage their datasets. This suite provides
       MPI-based tools to handle typical jobs like copy, remove, and compare
       for such datasets, providing speedups of up to 20-30x."""

    homepage = "https://github.com/hpc/mpifileutils"
    url      = "https://github.com/hpc/mpifileutils/archive/v0.9.tar.gz"
    git      = "https://github.com/hpc/mpifileutils.git"

    version('develop', branch='master')
    version('0.10.1', sha256='4c8409ef4140f6f557d0e93f0c1267baf5d893c203b29fb7a33d9bc3c5a5d25c')
    version('0.10',   sha256='5a71a9acd9841c3c258fc0eaea942f18abcb40098714cc90462b57696c07e3c5')
    version('0.9.1',  sha256='15a22450f86b15e7dc4730950b880fda3ef6f59ac82af0b268674d272aa61c69')
    version('0.9',    sha256='1b8250af01aae91c985ca5d61521bfaa4564e46efa15cee65cd0f82cf5a2bcfb')

    patch('nosys_getdents.patch', when='@:0.10.1 target=aarch64:')

    conflicts('platform=darwin')

    depends_on('mpi')
    depends_on('libcircle@0.3:')

    # need precise version of dtcmp, since DTCMP_Segmented_exscan added
    # in v1.0.3 but renamed in v1.1.0 and later
    depends_on('dtcmp@1.0.3',  when='@:0.7')
    depends_on('dtcmp@1.1.0:', when='@0.8:')

    depends_on('libarchive')

    depends_on('cmake@3.1:', when='@0.9:', type='build')

    variant('xattr', default=True,
            description="Enable code for extended attributes")

    variant('lustre', default=False,
            description="Enable optimizations and features for Lustre")

    variant('gpfs', default=False,
            description="Enable optimizations and features for GPFS")
    conflicts('+gpfs', when='@:0.8.1')

    variant('experimental', default=False,
            description="Install experimental tools")
    conflicts('+experimental', when='@:0.6')

    def cmake_args(self):
        args = std_cmake_args
        args.append('-DCMAKE_INSTALL_PREFIX=%s' % self.spec.prefix)
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

    @when('@0.9:')
    def install(self, spec, prefix):
        args = self.cmake_args()

        source_directory = self.stage.source_path
        build_directory = join_path(source_directory, 'build')

        with working_dir(build_directory, create=True):
            cmake(source_directory, *args)
            make()
            make('install')

        if self.run_tests:
            make('test')

    def configure_args(self):
        args = []
        args.append('--prefix=%s' % self.spec.prefix)
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

        if self.spec.satisfies('@0.7:'):
            if '+experimental' in self.spec:
                args.append('--enable-experimental')
            else:
                args.append('--disable-experimental')
        return args

    @when('@:0.8.1')
    def install(self, spec, prefix):
        args = self.configure_args()

        configure(*args)
        make()
        make('install')

        if self.run_tests:
            make('test')
