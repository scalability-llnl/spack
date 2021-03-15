# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import subprocess

from spack import *

releases = {
    '2021.1.1': {'irc_id': '17397', 'build': '76'}}


class IntelOneapiMpi(IntelOneApiLibraryPackage):
    """Intel oneAPI MPI."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/mpi-library.html'

    version('2021.1.1', sha256='8b7693a156c6fc6269637bef586a8fd3ea6610cac2aae4e7f48c1fbb601625fe', expand=False)

    provides('mpi@:3')

    depends_on('patchelf', type='build')

    def __init__(self, spec):
        self.component_info(dir_name='mpi',
                            components='intel.oneapi.lin.mpi.devel',
                            releases=releases,
                            url_name='mpi_oneapi')
        super(IntelOneapiMpi, self).__init__(spec)

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
        for dir in ['lib/release_mt', 'lib', 'libfabric/lib']:
            lib_path = '{0}/{1}/latest/{2}'.format(self.prefix, self._dir_name, dir)
            ldir = find_libraries('*', root=lib_path, shared=True, recursive=False)
            libs += ldir
        return libs

    def _join_prefix(self, path):
        return join_path(self.prefix, 'mpi', 'latest', path)

    def _ld_library_path(self):
        dirs = ['lib',
                'lib/release',
                'libfabric/lib']
        for dir in dirs:
            yield self._join_prefix(dir)

    def _library_path(self):
        dirs = ['lib',
                'lib/release',
                'libfabric/lib']
        for dir in dirs:
            yield self._join_prefix(dir)

    def install(self, spec, prefix):
        super(IntelOneapiMpi, self).install(spec, prefix)

        # need to patch libmpi.so so it can always find libfabric
        libfabric_rpath = self._join_prefix('libfabric/lib')
        for lib_version in ['debug', 'release', 'release_mt', 'debug_mt']:
            file = self._join_prefix('lib/' + lib_version + '/libmpi.so')
            subprocess.call(['patchelf', '--set-rpath', libfabric_rpath, file])
        subprocess.call(['sed', '-i', '-e', 
                         's/icc|icpc|dpcpp/icc|icpc|dpcpp|icx|icpx/g',
                         self._join_prefix('bin/mpicxx')])

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self._join_prefix('bin'))
        env.prepend_path('CPATH', self._join_prefix('include'))
        for dir in self._library_path():
            env.prepend_path('LIBRARY_PATH', dir)
        for dir in self._ld_library_path():
            env.prepend_path('LD_LIBRARY_PATH', dir)
        # so wrappers know where MPI lives
        mpi_root = join_path(prefix, 'mpi', 'latest')
        env.set('I_MPI_ROOT', mpi_root)
        # set this so that wrappers can find libfabric providers
        env.set('FI_PROVIDER_PATH', self._join_prefix('libfabric/lib/prov'))
