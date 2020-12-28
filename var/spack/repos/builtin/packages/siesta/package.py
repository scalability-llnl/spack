# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Siesta(Package):
    """SIESTA performs electronic structure calculations and ab initio molecular
       dynamics simulations of molecules and solids."""

    homepage = "https://departments.icmab.es/leem/siesta/"

    version('4.0.1', sha256='bfb9e4335ae1d1639a749ce7e679e739fdead5ee5766b5356ea1d259a6b1e6d1', url='https://launchpad.net/siesta/4.0/4.0.1/+download/siesta-4.0.1.tar.gz')
    version('3.2-pl-5', sha256='e438bb007608e54c650e14de7fa0b5c72562abb09cbd92dcfb5275becd929a23', url='http://departments.icmab.es/leem/siesta/CodeAccess/Code/siesta-3.2-pl-5.tgz')

    patch('configure.patch', when='@:4.0')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        sh = which('sh')
        configure_args = ['--enable-mpi',
                          '--with-blas=%s' % spec['blas'].libs,
                          '--with-lapack=%s' % spec['lapack'].libs,
                          # need to include BLAS below because Intel MKL's
                          # BLACS depends on BLAS, otherwise the compiler
                          # test fails
                          '--with-blacs=%s' % (spec['scalapack'].libs +
                                               spec['blas'].libs),
                          '--with-scalapack=%s' % spec['scalapack'].libs,
                          '--with-netcdf=%s' % (spec['netcdf-fortran'].libs +
                                                spec['netcdf-c'].libs),
                          # need to specify MPIFC explicitly below, otherwise
                          # Intel's mpiifort is not found
                          'MPIFC=%s' % spec['mpi'].mpifc
                          ]
        for d in ['Obj', 'Obj_trans']:
            with working_dir(d, create=True):
                sh('../Src/configure', *configure_args)
                if spec.satisfies('@:4.0%intel'):
                    with open('arch.make', 'a') as f:
                        f.write('\natom.o: atom.F\n')
                        f.write('\t$(FC) -c $(FFLAGS) -O1')
                        f.write('$(INCFLAGS) $(FPPFLAGS) $<')
                sh('../Src/obj_setup.sh')

    def build(self, spec, prefix):
        with working_dir('Obj'):
            make(parallel=False)
        with working_dir('Obj_trans'):
            make('transiesta', parallel=False)
        with working_dir('Util'):
            sh = which('sh')
            sh('build_all.sh')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir('Obj'):
            install('siesta', prefix.bin)
        with working_dir('Obj_trans'):
            install('transiesta', prefix.bin)
        for root, _, files in os.walk('Util'):
            for fname in files:
                fname = join_path(root, fname)
                if os.access(fname, os.X_OK):
                    install(fname, prefix.bin)
