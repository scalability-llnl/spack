# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os.path

from spack.package import *


class Plumed(AutotoolsPackage):
    """PLUMED is an open source library for free energy calculations in
    molecular systems which works together with some of the most popular
    molecular dynamics engines.

    Free energy calculations can be performed as a function of many order
    parameters with a particular focus on biological problems, using state
    of the art methods such as metadynamics, umbrella sampling and
    Jarzynski-equation based steered MD.

    The software, written in C++, can be easily interfaced with both fortran
    and C/C++ codes.
    """
    homepage = 'http://www.plumed.org/'
    url = 'https://github.com/plumed/plumed2/archive/v2.5.3.tar.gz'
    git = 'https://github.com/plumed/plumed2.git'

    version('master', branch='master')
    version('2.6.2', preferred=True, sha256='bbc2ef0cb08d404513b8b737c72333b6656389e15effd6a0f9ace2a5758c9a4a')
    version('2.6.1', sha256='c1b3c397b2d971140aa240dde50e48a04ce78e3dedb02b6dca80fa53f8026e4e')
    version('2.6.0', sha256='3d57ae460607a49547ef38a52c4ac93493a3966857c352280a9c05f5dcdb1820')
    version('2.5.5', sha256='70faa9ff1938e286dc388cb793b39840953e5646855b684f48df1bc864b737e8')
    version('2.5.4', sha256='a1647e598191f261e75d06351e607475d395af481315052a4c28563ac9989a7f')
    version('2.5.3', sha256='543288be667dc4201fc461ecd2dd4878ddfbeac682d0c021c99ea8e501c7c9dc')
    version('2.5.2', sha256='85d10cc46e2e37c7719cf51c0931278f56c2c8f8a9d86188b2bf97c2535a2ab4')
    version('2.5.1', sha256='de309980dcfd6f6e0e70e138856f4bd9eb4d8a513906a5e6389f18a5af7f2eba')
    version('2.5.0', sha256='53e08187ec9f8af2326fa84407e34644a7c51d2af93034309fb70675eee5e4f7')
    version('2.4.6', sha256='c22ad19f5cd36ce9fe4ba0b53158fc2a3d985c48fc04606e3f3b3e835b994cb3')
    version('2.4.4', sha256='1e5c24109314481fad404da97d61c7339b219e27e120c9c80bacc79c9f6a51a8')
    version('2.4.2', sha256='528ce57f1f5330480bcd403140166a4580efd2acaea39c85dfeca5e2cd649321')
    version('2.4.1', sha256='f00410ebdd739c2ddf55fcd714ff4bd88a1029e02d2fc9cea0b5fca34e0fc4eb')
    version('2.3.5', sha256='a6a66ca4582c1aecc6138c96be015e13cd06a718e8446b2f13e610fe34602e4f')
    version('2.3.3', sha256='ac058ff529f207d5b4169fb5a87bdb3c77307dfef1ac543ad8b6c74c5de7fc91')
    version('2.3.0', sha256='b1c8a54a313a0569e27e36420770074f35406453f73de70e55c424652abeddf1')
    version('2.2.4', sha256='d7a1dba34a7fe03f23e8d39ab6e15b230c4851373fdceb3602e2de26ea53ce37')
    version('2.2.3', sha256='2db19c5f6a2918833941d0bf47b5431d0865529d786df797ccc966d763ed7b0c')

    # Variants. PLUMED by default builds a number of optional modules.
    # The ones listed here are not built by default for various reasons,
    # such as stability, lack of testing, or lack of demand.
    # FIXME: This needs to be an optional
    variant(
        'optional_modules',
        default='all',
        values=lambda x: True,
        description='String that is used to build optional modules'
    )
    variant('shared', default=True, description='Builds shared libraries')
    variant('mpi', default=True, description='Activates MPI support')
    variant('gsl', default=True, description='Activates GSL support')

    # Dependencies. LAPACK and BLAS are recommended but not essential.
    depends_on('zlib')
    depends_on('blas')
    depends_on('lapack')
    # For libmatheval support through the 'function' module
    # which is enabled by default (or when optional_modules=all)
    depends_on('libmatheval', when='@:2.4.99')

    depends_on('mpi', when='+mpi')
    depends_on('gsl', when='+gsl')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('py-cython', type='build', when='@2.5:')

    force_autoreconf = True

    parallel = False

    def apply_patch(self, other):

        # The name of MD engines differ slightly from the ones used in Spack
        format_strings = collections.defaultdict(
            lambda: '{0.name}-{0.version}'
        )
        format_strings['espresso'] = 'q{0.name}-{0.version}'
        format_strings['amber'] = '{0.name}{0.version}'

        get_md = lambda x: format_strings[x.name].format(x)

        # Get available patches
        plumed_patch = Executable(
            os.path.join(self.spec.prefix.bin, 'plumed-patch')
        )

        out = plumed_patch('-q', '-l', output=str)
        available = out.split(':')[-1].split()

        # Check that `other` is among the patchable applications
        if get_md(other) not in available:
            msg = '{0.name}@{0.version} is not among the MD engine'
            msg += ' that can be patched by {1.name}@{1.version}.\n'
            msg += 'Supported engines are:\n'
            for x in available:
                msg += x + '\n'
            raise RuntimeError(msg.format(other, self.spec))

        # Call plumed-patch to patch executables
        target = format_strings[other.name].format(other)
        plumed_patch('-p', '-e', target)

    def setup_dependent_package(self, module, dependent_spec):
        # Make plumed visible from dependent packages
        module.plumed = dependent_spec['plumed'].command

    @property
    def plumed_inc(self):
        return os.path.join(
            self.prefix.lib, 'plumed', 'src', 'lib', 'Plumed.inc'
        )

    @run_before('autoreconf')
    def filter_gslcblas(self):
        # This part is needed to avoid linking with gsl cblas
        # interface which will mask the cblas interface
        # provided by optimized libraries due to linking order
        filter_file('-lgslcblas', '', 'configure.ac')

    def configure_args(self):
        spec = self.spec

        # From plumed docs :
        # Also consider that this is different with respect to what some other
        # configure script does in that variables such as MPICXX are
        # completely ignored here. In case you work on a machine where CXX is
        # set to a serial compiler and MPICXX to a MPI compiler, to compile
        # with MPI you should use:
        #
        # > ./configure CXX="$MPICXX"

        # The configure.ac script may detect the wrong linker for
        # LD_RO which causes issues at link time. Here we work around
        # the issue saying we have no LD_RO executable.
        configure_opts = ['--disable-ld-r']

        # If using MPI then ensure the correct compiler wrapper is used.
        if '+mpi' in spec:
            configure_opts.extend([
                '--enable-mpi',
                'CXX={0}'.format(spec['mpi'].mpicxx)
            ])

            # If the MPI dependency is provided by the intel-mpi package then
            # the following additional argument is required to allow it to
            # build.
            if 'intel-mpi' in spec:
                configure_opts.extend([
                    'STATIC_LIBS=-mt_mpi'
                ])

        # Set flags to help find gsl
        if '+gsl' in self.spec:
            gsl_libs = self.spec['gsl'].libs
            blas_libs = self.spec['blas'].libs
            configure_opts.append('LDFLAGS={0}'.format(
                (gsl_libs + blas_libs).ld_flags
            ))

        # Additional arguments
        configure_opts.extend([
            '--enable-shared={0}'.format('yes' if '+shared' in spec else 'no'),
            '--enable-gsl={0}'.format('yes' if '+gsl' in spec else 'no')
        ])

        # Construct list of optional modules

        # If we have specified any optional modules then add the argument to
        # enable or disable them.
        optional_modules = self.spec.variants['optional_modules'].value
        if optional_modules:
            # From 'configure --help' @2.3:
            # all/none/reset or : separated list such as
            # +crystallization:-bias default: reset
            configure_opts.append(
                '--enable-modules={0}'.format(optional_modules)
            )

        return configure_opts
