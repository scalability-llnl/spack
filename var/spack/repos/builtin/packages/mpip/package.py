# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpip(AutotoolsPackage):

    """mpiP: Lightweight, Scalable MPI Profiling"""
    homepage = "https://software.llnl.gov/mpiP/"
    url      = "https://github.com/LLNL/mpiP/releases/download/3.5/mpip-3.5.tgz"
    git      = "https://github.com/llnl/mpip.git"
    maintainers = ['cchambreau']

    version('master', branch='master')
    version('3.5',
            sha256="e366843d53fa016fb03903e51c8aac901aa5155edabe64698a8d6fa618a03bbd")
    version("3.4.1",
            sha256="66a86dafde61546be80a130c46e4295f47fb764cf312ae62c70a6dc456a59dac")

    variant('demangling', default=True,
            description="Build with demangling support")

    variant('setjmp', default=False,
            description="Use setjmp to generate stack trace")

    variant('mpi_io', default=True,
            description="Enable MPI-I/O reporting")

    variant('mpi_rma', default=True,
            description="Enable MPI RMA reporting")

    variant('mpi_nbc', default=True,
            description="Enable MPI non-blocking collective reporting")

    variant('bfd', default=True,
            description="Enable GNU binutils libbfd for source lookup")

    variant('libunwind', default=True,
            description="Use libunwind togenerate stack trace")

    variant('maxargs', values=int, default=32,
            description='Set number of command line arguments in report')

    variant('stackdepth', values=int, default=8,
            description='Specify maximum report stacktrace depth')

    variant('internal_stackdepth', values=int, default=3,
            description='Specify number of internal stack frames')

    variant('add_shared_target', default=False, description="Add shared make target")

    conflicts('platform=darwin')

    # make-wrappers.py wrapper generator script requires python
    depends_on('python@2:', when='@3.5:', type='build')
    depends_on('python@:2', when='@3.4.1', type='build')
    depends_on('mpi')

    #  Ideally would use libunwind, but provide backtrace and
    #    setjmp functionality, if needed
    #  depends_on('unwind')

    @when('@3.5:')
    def configure_args(self):
        spec = self.spec

        config_args = []
        config_args.append("--with-cc=%s" % spec['mpi'].mpicc)
        config_args.append("--with-cxx=%s" % spec['mpi'].mpicxx)
        config_args.append("--with-f77=%s" % spec['mpi'].mpif77)

        #  mpiP checks for libiberty demangling during configure.
        #  Current mpiP configure functionality allows specifying alternate
        #  demangling support (IBM, Compaq) as an argument, but the usefulness
        #  of this is not clear.
        #
        #  Since, --enable-demangling doesn't do anything,
        #  providing --disable-demangling in the event that there is an error
        #  with demangling.
        if '-demangling' in spec:
            config_args.append('--disable-demangling')

        if '-mpi_io' in spec:
            config_args.append('--disable-mpi-io')

        if '-mpi_rma' in spec:
            config_args.append('--disable-mpi-rma')

        if '-mpi_nbc' in spec:
            config_args.append('--disable-mpi-nbc')

        if '-bfd' in spec:
            config_args.append('--disable-bfd')

        if '-libunwind' in spec:
            config_args.append('--disable-libunwind')

        #  Simply enabling setjmp may result in libunwind being used,
        #  if available.  Adding --disable-libunwind to ensure setjmp is used.
        if '+setjmp' in spec:
            config_args.append('--disable-libunwind')
            config_args.append('--enable-setjmp')

        maxargs = int(spec.variants['maxargs'].value)
        config_args.extend(['--enable-maxargs={0}'.format(maxargs)])

        stackdepth = int(spec.variants['stackdepth'].value)
        config_args.extend(['--enable-stackdepth={0}'.format(stackdepth)])

        internal_stackdepth = int(spec.variants['internal_stackdepth'].value)
        config_args.extend(['--enable-internal-stackdepth={0}'
                           .format(internal_stackdepth)])
        return config_args

    #  Support 3.4.1 'shared' target for building shared library
    @property
    def build_targets(self):
        targets = []
        if '+add_shared_target' in self.spec:
            targets.append('shared')

        return targets

    @when('@3.4.1')
    def configure_args(self):
        config_args = ['--without-f77']
        config_args.append("--with-cc=%s" % self.spec['mpi'].mpicc)
        config_args.append("--with-cxx=%s" % self.spec['mpi'].mpicxx)

        if '+demangling' in self.spec:
            config_args.append('--enable-demangling')
        else:
            config_args.append('--disable-demangling')

        if '+setjmp' in self.spec:
            config_args.append('--enable-setjmp')
        else:
            config_args.append('--disable-setjmp')

        return config_args
