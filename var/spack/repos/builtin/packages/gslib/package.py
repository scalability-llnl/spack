# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gslib(Package):
    """Highly scalable Gather-scatter code with AMG and XXT solvers"""

    homepage = "https://github.com/gslib/gslib"
    git      = "https://github.com/gslib/gslib.git"

    version('develop', branch='master')
    version('1.0.6', tag='v1.0.6')
    version('1.0.5', tag='v1.0.5')
    version('1.0.4', tag='v1.0.4')
    version('1.0.3', tag='v1.0.3')
    version('1.0.2', tag='v1.0.2')
    version('1.0.1', tag='v1.0.1')
    version('1.0.0', tag='v1.0.0')

    variant('mpi', default=True, description='Build with MPI')
    variant('mpiio', default=True, description='Build with MPI I/O')
    variant('blas', default=False, description='Build with BLAS')

    depends_on('mpi', when="+mpi")
    depends_on('mpi', when="+mpiio")
    depends_on('blas', when="+blas")

    conflicts('~mpi', when='+mpiio')

    def install(self, spec, prefix):
        src_dir = 'src'
        lib_dir = 'lib'
        libname = 'libgs.a'

        if self.spec.satisfies('@1.0.1:'):
            makefile = 'Makefile'
        else:
            makefile = 'src/Makefile'

        cc  = self.compiler.cc

        if '+mpiio' not in spec:
            filter_file(r'MPIIO.*?=.*1', 'MPIIO = 0', makefile)

        if '+mpi' in spec:
            cc  = spec['mpi'].mpicc
        else:
            filter_file(r'MPI.*?=.*1', 'MPI = 0', makefile)
            filter_file(r'MPIIO.*?=.*1', 'MPIIO = 0', makefile)

        make_cmd = "CC=" + cc

        if '+blas' in spec:
            filter_file(r'BLAS.*?=.*0', 'BLAS = 1', makefile)
            blas = spec['blas'].libs
            ld_flags = blas.ld_flags
            filter_file(r'\$\(LDFLAGS\)', ld_flags, makefile)

        if self.spec.satisfies('@1.0.3:'):
            make(make_cmd)
            make('install', 'INSTALL_ROOT=%s' % self.prefix)
        else:
            if self.spec.satisfies('@1.0.1:'):
                make(make_cmd)
                make('install')
                install_tree(lib_dir, prefix.lib)
            elif self.version == Version('1.0.0'):
                with working_dir(src_dir):
                    make(make_cmd)
                    mkdir(prefix.lib)
                    install(libname, prefix.lib)
            # Should only install the headers (this will be fixed in gslib on
            # future releases).
            install_tree(src_dir, prefix.include)
