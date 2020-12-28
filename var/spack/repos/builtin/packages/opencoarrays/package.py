# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opencoarrays(CMakePackage):
    """OpenCoarrays is an open-source software project that produces an
    application binary interface (ABI) supporting coarray Fortran (CAF)
    compilers, an application programming interface (API) that supports users
    of non-CAF compilers, and an associated compiler wrapper and program
    launcher.
    """

    homepage = "http://www.opencoarrays.org/"
    url      = "https://github.com/sourceryinstitute/OpenCoarrays/releases/download/2.2.0/OpenCoarrays-2.2.0.tar.gz"

    version('2.7.1', sha256='d74ee914f94de1c396b96bbad2cf43d68f29fcc87460fcc0db6582e6ae691588')
    version('2.2.0', sha256='9311547a85a21853111f1e8555ceab4593731c6fd9edb64cfb9588805f9d1a0d')
    version('1.8.10', sha256='69b61d2d3b171a294702efbddc8a602824e35a3c49ee394b41d7fb887001501a')
    version('1.8.4', sha256='0cde7b114fa6d2d5eac55ace4f709e3b5eb7c7a33b81ddcaa3aaf01b2f486c0c')
    version('1.8.0', sha256='96f5a9c37f7bb587eacd44bc8789924d20c8e56dbbc51fad57e73d9f7a3768b5')
    version('1.7.4', sha256='1929dee793ce8f09e3b183e2b07c3e0008580cc76b460b1f7f7c066ad6672e14')
    version('1.6.2', sha256='7855d42a01babc233a070cc87282b5f8ffd538a7c87ec5119605d4d7c6d7f67e')

    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'MinSizeRel', 'CodeCoverage'))

    depends_on('mpi')
    # This patch removes a bunch of checks for the version of MPI available on
    # the system. They make the Crays hang.
    patch('CMakeLists.patch', when='platform=cray')

    def cmake_args(self):
        args = []
        args.append("-DCMAKE_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        args.append("-DCMAKE_Fortran_COMPILER=%s" % self.spec['mpi'].mpifc)
        return args
