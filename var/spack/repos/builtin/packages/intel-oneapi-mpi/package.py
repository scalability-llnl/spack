# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from os import path
import subprocess
from sys import platform


from spack import *


class IntelOneapiMpi(IntelOneApiLibraryPackage):
    """Intel oneAPI MPI."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/mpi-library.html'

    if platform == 'linux':
        version('2021.1.1',
                sha256='8b7693a156c6fc6269637bef586a8fd3ea6610cac2aae4e7f48c1fbb601625fe',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17397/l_mpi_oneapi_p_2021.1.1.76_offline.sh',
                expand=False)

    provides('mpi@:3')

    depends_on('patchelf', type='build')

    @property
    def component_dir(self):
        return 'mpi'

    def setup_dependent_package(self, module, dep_spec):
        dir = join_path(self.prefix, 'mpi', 'latest', 'bin')
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

    @property
    def libs(self):
        libs = []
        for dir in [path.join('lib', 'release_mt'),
                    'lib',
                    path.join('libfabric', 'lib')]:
            lib_path = path.join(self.prefix, 'mpi', 'latest', dir)
            ldir = find_libraries('*', root=lib_path, shared=True, recursive=False)
            libs += ldir
        return libs

    def _join_prefix(self, path):
        return join_path(self.prefix, 'mpi', 'latest', path)

    def install(self, spec, prefix):
        super(IntelOneapiMpi, self).install(spec, prefix)

        # need to patch libmpi.so so it can always find libfabric
        libfabric_rpath = self._join_prefix(path.join('libfabric', 'lib'))
        for lib_version in ['debug', 'release', 'release_mt', 'debug_mt']:
            file = self._join_prefix(path.join('lib', lib_version, 'libmpi.so'))
            subprocess.call(['patchelf', '--set-rpath', libfabric_rpath, file])
