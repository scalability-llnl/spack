# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Mpifileutils(CMakePackage):
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

    version('develop', branch='master')
    version('0.10',  sha256='5a71a9acd9841c3c258fc0eaea942f18abcb40098714cc90462b57696c07e3c5')
    version('0.9.1', sha256='15a22450f86b15e7dc4730950b880fda3ef6f59ac82af0b268674d272aa61c69')
    version('0.9',   sha256='1b8250af01aae91c985ca5d61521bfaa4564e46efa15cee65cd0f82cf5a2bcfb')

    conflicts('platform=darwin')

    depends_on('mpi')
    depends_on('libcircle@0.3:')
    depends_on('dtcmp@1.1.0:')
    depends_on('libarchive')

    depends_on('cmake@3.1:', type='build')

    variant('xattr', default=True,
            description="Enable code for extended attributes")

    variant('lustre', default=False,
            description="Enable optimizations and features for Lustre")

    variant('gpfs', default=False,
            description="Enable optimizations and features for GPFS")

    variant('experimental', default=False,
            description="Install experimental tools")

    def cmake_args(self):
        args = [
            "-DWITH_DTCMP_PREFIX=%s" % self.spec['dtcmp'].prefix,
            "-DWITH_LibCircle_PREFIX=%s" % self.spec['libcircle'].prefix
        ]

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
