# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Dftbplus(MakefilePackage):
    """DFTB+ is an implementation of the
    Density Functional based Tight Binding (DFTB) method,
    containing many extensions to the original method."""

    homepage = "https://www.dftbplus.org"
    url      = "https://github.com/dftbplus/dftbplus/archive/19.1.tar.gz"

    version('19.1', sha256='4d07f5c6102f06999d8cfdb1d17f5b59f9f2b804697f14b3bc562e3ea094b8a8')

    resource(name='slakos',
             url='https://github.com/dftbplus/testparams/archive/dftbplus-18.2.tar.gz',
             sha256='bd191b3d240c1a81a8754a365e53a78b581fc92eb074dd5beb8b56a669a8d3d1',
             destination='external/slakos',
             when='@18.2:')

    variant('mpi', default=True,
            description="Build an MPI-paralelised version of the code.")

    variant('gpu', default=False,
            description="Use the MAGMA library "
            "for GPU accelerated computation")

    variant('elsi', default=False,
            description="Use the ELSI library for large scale systems. "
            "Only has any effect if you build with '+mpi'")

    variant('sockets', default=False,
            description="Whether the socket library "
            "(external control) should be linked")

    variant('arpack', default=False,
            description="Use ARPACK for excited state DFTB functionality")

    variant('transport', default=False,
            description="Whether transport via libNEGF should be included. "
            "Only affects parallel build. "
            "(serial version is built without libNEGF/transport)")

    variant('dftd3', default=False,
            description="Use DftD3 dispersion library "
            "(if you need this dispersion model)")

    depends_on('lapack')
    depends_on('blas')
    depends_on('scalapack', when="+mpi")
    depends_on('mpi', when="+mpi")
    depends_on('elsi', when="+elsi")
    depends_on('magma', when="+gpu")
    depends_on('arpack-ng', when="+arpack")
    depends_on('dftd3-lib@0.9.2', when="+dftd3")

    def edit(self, spec, prefix):
        """
        First, change the ROOT variable, because, for some reason,
        the Makefile and the spack install script run in different directories

        Then, if using GCC, rename the file 'sys/make.x86_64-linux-gnu'
        to make.arch.

        After that, edit the make.arch to point to the dependencies

        And the last thing we do here is to set the installdir
        """
        dircwd = os.getcwd()
        makefile = FileFilter("makefile")
        makefile.filter("ROOT := .*", "ROOT := {0}".format(dircwd))

        archmake = join_path(".", "sys", "make.x86_64-linux-gnu")
        copy(archmake, join_path(dircwd, "make.arch"))

        march = FileFilter(join_path(dircwd, 'make.arch'))

        mconfig = FileFilter(join_path(dircwd, 'make.config'))

        mconfig.filter('INSTALLDIR := .*', 'INSTALLDIR := {0}'.format(prefix))

        if '+gpu' in self.spec:
            march.filter('MAGMADIR = .*',
                         'MAGMADIR = {0}'.format(spec['magma'].prefix))

            mconfig.filter('WITH_GPU := .*', 'WITH_GPU := 1')

        if '+mpi' in self.spec:
            march.filter('SCALAPACKDIR = .*',
                         'SCALAPACKDIR = {0}'.format(spec['scalapack'].prefix))

            march.filter('LIB_LAPACK = -l.*',
                         'LIB_LAPACK = {0}'.format(spec['blas'].libs.ld_flags))

            march.filter('mpifort', '{0}'.format(spec['mpi'].mpifc))

            mconfig.filter('WITH_MPI := .*', 'WITH_MPI := 1')

            if '+elsi' in self.spec:
                mconfig.filter('WITH_ELSI := .*', 'WITH_ELSI := 1')

                has_pexsi = '+enable_pexsi' in spec['elsi']

                mconfig.filter('WITH_PEXSI := .*', 'WITH_PEXSI := {0}'.format(
                    '1' if has_pexsi is True else '0'
                ))

                march.filter("ELSIINCDIR .*", "ELSIINCDIR = {0}".format(
                    spec['elsi'].prefix.include
                ))

                march.filter("ELSIDIR .*",
                             "ELSIDIR = {0}".format(spec['elsi'].prefix))

        else:
            march.filter('LIB_LAPACK += -l.*', 'LIB_LAPACK += {0}'.format(
                spec['blas'].libs.ld_flags))

        if '+sockets' in self.spec:
            mconfig.filter('WITH_SOCKETS := .*', 'WITH_SOCKETS := 1')

        if '+transport' in self.spec:
            mconfig.filter('WITH_TRANSPORT := .*', 'WITH_TRANSPORT := 1')

        if '+arpack' in self.spec:
            march.filter('ARPACK_LIBS = .*', 'ARPACK_LIBS = {0}'.format(
                spec['arpack-ng'].libs.ld_flags
            ))

            mconfig.filter('WITH_ARPACK := .*', 'WITH_ARPACK := 1')

        if '+dftd3' in self.spec:
            march.filter('COMPILE_DFTD3 = .*', 'COMPILE_DFTD3 = 0')
            march.filter('DFTD3_INCS = .*', 'DFTD3_INCS = -I{0}'.format(
                spec['dftd3-lib'].prefix.include
            ))

            march.filter('DFTD3_LIBS = .*',
                         'DFTD3_LIBS = -L{0} -ldftd3'.format(
                             spec['dftd3-lib'].prefix))

            mconfig.filter('WITH_DFTD3 := .*', 'WITH_DFTD3 := 1')
