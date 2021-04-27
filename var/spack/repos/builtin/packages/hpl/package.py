# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import platform


class Hpl(AutotoolsPackage):
    """HPL is a software package that solves a (random) dense linear system
    in double precision (64 bits) arithmetic on distributed-memory computers.
    It can thus be regarded as a portable as well as freely available
    implementation of the High Performance Computing Linpack Benchmark."""

    homepage = "http://www.netlib.org/benchmark/hpl/"
    url      = "http://www.netlib.org/benchmark/hpl/hpl-2.2.tar.gz"

    # Note: HPL uses autotools starting with 2.3

    version('2.3', sha256='32c5c17d22330e6f2337b681aded51637fb6008d3f0eb7c277b163fadd612830')
    version('2.2', sha256='ac7534163a09e21a5fa763e4e16dfc119bc84043f6e6a807aba666518f8df440')

    variant('openmp', default=False, description='Enable OpenMP support')

    depends_on('mpi@1.1:')
    depends_on('blas')

    # 2.3 adds support for openmpi 4
    conflicts('^openmpi@4.0.0:', when='@:2.2')

    parallel = False

    arch = '{0}-{1}'.format(platform.system(), platform.processor())
    build_targets = ['arch={0}'.format(arch)]

    @when('@:2.2')
    def autoreconf(self, spec, prefix):
        # Prevent sanity check from killing the build
        touch('configure')

    @when('@:2.2')
    def configure(self, spec, prefix):
        # List of configuration options
        # Order is important
        config = []

        # OpenMP support
        if '+openmp' in spec:
            config.append(
                'OMP_DEFS     = {0}'.format(self.compiler.openmp_flag)
            )

        config.extend([
            # Shell
            'SHELL        = /bin/sh',
            'CD           = cd',
            'CP           = cp',
            'LN_S         = ln -fs',
            'MKDIR        = mkdir -p',
            'RM           = /bin/rm -f',
            'TOUCH        = touch',
            # Platform identifier
            'ARCH         = {0}'.format(self.arch),
            # HPL Directory Structure / HPL library
            'TOPdir       = {0}'.format(os.getcwd()),
            'INCdir       = $(TOPdir)/include',
            'BINdir       = $(TOPdir)/bin/$(ARCH)',
            'LIBdir       = $(TOPdir)/lib/$(ARCH)',
            'HPLlib       = $(LIBdir)/libhpl.a',
            # Message Passing library (MPI)
            'MPinc        = {0}'.format(spec['mpi'].prefix.include),
            'MPlib        = -L{0}'.format(spec['mpi'].prefix.lib),
            # Linear Algebra library (BLAS or VSIPL)
            'LAinc        = {0}'.format(spec['blas'].prefix.include),
            'LAlib        = {0}'.format(spec['blas'].libs.joined()),
            # F77 / C interface
            'F2CDEFS      = -DAdd_ -DF77_INTEGER=int -DStringSunStyle',
            # HPL includes / libraries / specifics
            'HPL_INCLUDES = -I$(INCdir) -I$(INCdir)/$(ARCH) ' +
            '-I$(LAinc) -I$(MPinc)',
            'HPL_LIBS     = $(HPLlib) $(LAlib) $(MPlib)',
            'HPL_OPTS     = -DHPL_DETAILED_TIMING -DHPL_PROGRESS_REPORT',
            'HPL_DEFS     = $(F2CDEFS) $(HPL_OPTS) $(HPL_INCLUDES)',
            # Compilers / linkers - Optimization flags
            'CC           = {0}'.format(spec['mpi'].mpicc),
            'CCNOOPT      = $(HPL_DEFS)',
            'CCFLAGS      = $(HPL_DEFS) -O3',
            'LINKER       = $(CC)',
            'LINKFLAGS    = $(CCFLAGS) $(OMP_DEFS)',
            'ARCHIVER     = ar',
            'ARFLAGS      = r',
            'RANLIB       = echo'
        ])

        # Write configuration options to include file
        with open('Make.{0}'.format(self.arch), 'w') as makefile:
            for var in config:
                makefile.write('{0}\n'.format(var))

    @when('@2.3:')
    def configure_args(self):
        filter_file(
            r"^libs10=.*", "libs10=%s" % self.spec["blas"].libs.ld_flags,
            "configure"
        )

        if '+openmp' in self.spec:
            config = ['CFLAGS=-O3 ' + self.compiler.openmp_flag]
        else:
            config = ['CFLAGS=-O3']

        if (self.spec.satisfies('^intel-mkl') or
            self.spec.satisfies('^intel-oneapi-mkl') or
            self.spec.satisfies('^intel-parallel-studio+mkl')):
            config.append('LDFLAGS={0}'.format(
                self.spec['blas'].libs.ld_flags))

        return config

    @when('@:2.2')
    def install(self, spec, prefix):
        # Manual installation
        install_tree(join_path('bin', self.arch), prefix.bin)
        install_tree(join_path('lib', self.arch), prefix.lib)
        install_tree(join_path('include', self.arch), prefix.include)
        install_tree('man', prefix.man)

    @run_after('install')
    def copy_dat(self):
        if self.spec.satisfies('@2.3:'):
            # The pre-2.3 makefile would include a default HPL.dat config
            # file in the bin directory
            install('./testing/ptest/HPL.dat',
                    join_path(self.prefix.bin, 'HPL.dat'))
