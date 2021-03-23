# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Unifyfs(AutotoolsPackage):
    """User level file system that enables applications to use node-local
    storage as burst buffers for shared files. Supports scalable and efficient
    aggregation of I/O bandwidth from burst buffers while having the same life
    cycle as a batch-submitted job.
    UnifyFS is designed to support common I/O workloads, including
    checkpoint/restart. While primarily designed for N-N write/read, UnifyFS
    compliments its functionality with the support for N-1 write/read."""

    homepage = "https://github.com/LLNL/UnifyFS"
    git      = "https://github.com/LLNL/UnifyFS.git"
    url      = "https://github.com/LLNL/UnifyFS/releases/download/v0.9.0/unifyfs-0.9.0.tar.gz"
    maintainers = ['CamStan']

    version('develop', branch='dev')
    version('0.9.1', sha256='2498a859cfa4961356fdf5c4c17e3afc3de7e034ad013b8c7145a622ef6199a0')
    version('0.9.0', sha256='e6c73e22ef1c23f3141646aa17058b69c1c4e526886771f8fe982da924265b0f')

    variant('auto-mount', default='True', description='Enable automatic mount/unmount in MPI_Init/Finalize')
    variant('hdf5', default='False', description='Build with parallel HDF5 (install with `^hdf5~mpi` for serial)')
    variant('fortran', default='False', description='Build with gfortran support')
    variant('mdhim', default='False', description='Enable MDHIM build options')
    variant('pmi', default='False', description='Enable PMI2 build options')
    variant('pmix', default='False', description='Enable PMIx build options')
    variant('spath', default='True', description='Use spath library to normalize relative paths')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')

    # Required dependencies
    depends_on('gotcha@1.0.3:', when='@0.9.1:')
    depends_on('mochi-margo@0.4.3')
    depends_on('mercury@1.0.1+bmi+sm')
    depends_on('mpi')
    depends_on('openssl')

    # Optional dependencies
    depends_on('hdf5', when='+hdf5')
    depends_on('leveldb', when='@0.9.1:+mdhim')
    depends_on('spath', when='@0.9.1:+spath')

    # Required dependencies for older versions
    depends_on('flatcc', when='@:0.9.0')
    depends_on('gotcha@0.0.2', when='@:0.9.0')
    depends_on('leveldb', when='@:0.9.0')

    patch('unifyfs-sysio.c.patch', when='@0.9.1')

    conflicts('^mercury~bmi')
    conflicts('^mercury~sm')
    # Known compatibility issues with ifort and xlf. Fixes coming.
    conflicts('%intel', when='+fortran')
    conflicts('%xl', when='+fortran')

    # Fix broken --enable-mpi-mount config option for version 0.9.0
    # See https://github.com/LLNL/UnifyFS/issues/467
    patch('auto-mount.patch', when='@0.9.0')

    # Parallel disabled to prevent tests from being run out-of-order when
    # installed with the --test={root, all} option.
    parallel = False
    debug_build = False
    build_directory = 'spack-build'

    # Only builds properly with debug symbols when flag_handler =
    # build_system_flags.
    # Override the default behavior in order to set debug_build which is used
    # to set the --disable-silent-rules option when configuring.
    def flag_handler(self, name, flags):
        if name in ('cflags', 'cppflags'):
            if '-g' in flags:
                self.debug_build = True
        return (None, None, flags)

    def configure_args(self):
        spec = self.spec
        args = []

        # UnifyFS's configure requires the exact path for HDF5
        def hdf5_compiler_path(name):
            if '~mpi' in spec[name]:  # serial HDF5
                return spec[name].prefix.bin.h5cc
            else:  # parallel HDF5
                return spec[name].prefix.bin.h5pcc

        args.extend(self.with_or_without('hdf5', hdf5_compiler_path))

        if '+auto-mount' in spec:
            args.append('--enable-mpi-mount')

        if '+fortran' in spec:
            args.append('--enable-fortran')

        if '+mdhim' in spec:
            args.append('--enable-mdhim')

        if '+pmi' in spec:
            args.append('--enable-pmi')

        if '+pmix' in spec:
            args.append('--enable-pmix')

        if self.debug_build:
            args.append('--disable-silent-rules')
        else:
            args.append('--enable-silent-rules')

        return args

    @when('@develop')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
