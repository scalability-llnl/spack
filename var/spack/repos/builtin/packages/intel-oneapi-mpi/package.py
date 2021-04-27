# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import subprocess
from sys import platform


from spack import *


class IntelOneapiMpi(IntelOneApiLibraryPackage):
    """Intel oneAPI MPI."""

    maintainers = ['rscohn2', 'danvev']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/mpi-library.html'

    if platform == 'linux':
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17729/l_mpi_oneapi_p_2021.2.0.215_offline.sh',
                sha256='d0d4cdd11edaff2e7285e38f537defccff38e37a3067c02f4af43a3629ad4aa3',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17397/l_mpi_oneapi_p_2021.1.1.76_offline.sh',
                sha256='8b7693a156c6fc6269637bef586a8fd3ea6610cac2aae4e7f48c1fbb601625fe',
                expand=False)

    provides('mpi@:3')

    depends_on('patchelf', type='build')

    @property
    def component_dir(self):
        return 'mpi'

    def setup_dependent_package(self, module, dep_spec):
        dir = join_path(self.component_path, 'bin')
        self.spec.mpicc  = join_path(dir, 'mpicc')
        self.spec.mpicxx = join_path(dir, 'mpicxx')
        self.spec.mpif77 = join_path(dir, 'mpif77')
        self.spec.mpifc  = join_path(dir, 'mpifc')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('MPICH_CC', spack_cc)
        env.set('MPICH_CXX', spack_cxx)
        env.set('MPICH_F77', spack_f77)
        env.set('MPICH_F90', spack_fc)
        env.set('MPICH_FC', spack_fc)

        # Set compiler wrappers for dependent build stage
        dir = join_path(self.component_path, 'bin')
        env.set('MPICC', join_path(dir, 'mpicc'))
        env.set('MPICXX', join_path(dir, 'mpicxx'))
        env.set('MPIF77', join_path(dir, 'mpif77'))
        env.set('MPIF90', join_path(dir, 'mpif90'))
        env.set('MPIFC', join_path(dir, 'mpifc'))

    @property
    def libs(self):
        libs = []
        for dir in [join_path('lib', 'release_mt'),
                    'lib',
                    join_path('libfabric', 'lib')]:
            lib_path = join_path(self.component_path, dir)
            ldir = find_libraries('*', root=lib_path, shared=True, recursive=False)
            libs += ldir
        return libs

    def install(self, spec, prefix):
        super(IntelOneapiMpi, self).install(spec, prefix)

        # need to patch libmpi.so so it can always find libfabric
        libfabric_rpath = join_path(self.component_path, 'libfabric', 'lib')
        for lib_version in ['debug', 'release', 'release_mt', 'debug_mt']:
            file = join_path(self.component_path, 'lib', lib_version, 'libmpi.so')
            subprocess.call(['patchelf', '--set-rpath', libfabric_rpath, file])
