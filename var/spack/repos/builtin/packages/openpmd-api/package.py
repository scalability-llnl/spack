# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OpenpmdApi(CMakePackage):
    """API for easy reading and writing of openPMD files"""

    homepage = "http://www.openPMD.org"
    url      = "https://github.com/openPMD/openPMD-api/archive/0.13.2.tar.gz"
    git      = "https://github.com/openPMD/openPMD-api.git"

    maintainers = ['ax3l']

    version('dev', branch='dev')
    version('0.13.2', sha256='2e5170d41bb7b2c0608ec833eee7f9adf8175b46734743f6e46dcce6f6685fb0')
    version('0.13.1', sha256='81ff79419982eb1b0865d1736f73f950f5d4c356d3c78200ceeab7f54dc07fd7')
    version('0.13.0', sha256='97c2e43d80ee5c5288f278bd54f0dcb40e7f48a575b278fcef9660214b779bb0')  # C++14 required
    # C++11 up until here
    version('0.12.0',  tag='0.12.0-alpha')
    version('0.11.1',  tag='0.11.1-alpha')

    variant('shared', default=True,
            description='Build a shared version of the library')
    variant('mpi', default=True,
            description='Enable parallel I/O')
    variant('hdf5', default=True,
            description='Enable HDF5 support')
    variant('adios1', default=False,
            description='Enable ADIOS1 support')
    variant('adios2', default=True,
            description='Enable ADIOS2 support')
    variant('python', default=False,
            description='Enable Python bindings')

    depends_on('cmake@3.15.0:', type='build')
    depends_on('mpark-variant@1.4.0:')
    depends_on('catch2@2.6.1:', type='test')
    depends_on('mpi@2.3:', when='+mpi')  # might become MPI 3.0+
    depends_on('hdf5@1.8.13:', when='+hdf5')
    depends_on('hdf5@1.8.13: ~mpi', when='~mpi +hdf5')
    depends_on('hdf5@1.8.13: +mpi', when='+mpi +hdf5')
    depends_on('adios@1.13.1: ~sz', when='+adios1')
    depends_on('adios@1.13.1: ~mpi ~sz', when='~mpi +adios1')
    depends_on('adios@1.13.1: +mpi ~sz', when='+mpi +adios1')
    depends_on('adios2@2.5.0:', when='+adios2')
    depends_on('adios2@2.6.0:', when='+adios2 @0.12.0:')
    depends_on('adios2@2.5.0: ~mpi', when='~mpi +adios2')
    depends_on('adios2@2.5.0: +mpi', when='+mpi +adios2')
    depends_on('nlohmann-json@3.9.1:')
    depends_on('py-pybind11@2.6.1:', when='+python', type='link')
    depends_on('py-numpy@1.15.1:', when='+python', type=['test', 'run'])
    depends_on('py-mpi4py@2.1.0:', when='+python +mpi', type=['test', 'run'])
    depends_on('python@3.6:', when='+python', type=['link', 'test', 'run'])

    extends('python', when='+python')

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            # variants
            self.define_from_variant('openPMD_USE_MPI', 'mpi'),
            self.define_from_variant('openPMD_USE_HDF5', 'hdf5'),
            self.define_from_variant('openPMD_USE_ADIOS1', 'adios1'),
            self.define_from_variant('openPMD_USE_ADIOS2', 'adios2'),
            self.define_from_variant('openPMD_USE_PYTHON', 'python'),
            # tests and examples
            self.define('BUILD_TESTING', self.run_tests),
            self.define('BUILD_EXAMPLES', self.run_tests)
        ]

        # switch internally shipped third-party libraries for spack
        if spec.satisfies('+python'):
            py_exe_define = 'Python_EXECUTABLE' \
                if spec.version >= Version('0.13.0') else 'PYTHON_EXECUTABLE'
            args += [
                self.define(py_exe_define, self.spec['python'].command.path),
                self.define('openPMD_USE_INTERNAL_PYBIND11', False)
            ]

        args += [
            self.define('openPMD_USE_INTERNAL_JSON', False),
            self.define('openPMD_USE_INTERNAL_VARIANT', False)
        ]
        if self.run_tests:
            args.append(self.define('openPMD_USE_INTERNAL_CATCH', False))

        return args

    def setup_run_environment(self, env):
        spec = self.spec
        # pre-load dependent CMake-PUBLIC header-only libs
        env.prepend_path('CMAKE_PREFIX_PATH', spec['mpark-variant'].prefix)
        env.prepend_path('CPATH', spec['mpark-variant'].prefix.include)

        # more deps searched in openPMDConfig.cmake
        if spec.satisfies("+mpi"):
            env.prepend_path('CMAKE_PREFIX_PATH', spec['mpi'].prefix)
        if spec.satisfies("+adios1"):
            env.prepend_path('CMAKE_PREFIX_PATH', spec['adios'].prefix)
            env.prepend_path('PATH', spec['adios'].prefix.bin)  # adios-config
        if spec.satisfies("+adios2"):
            env.prepend_path('CMAKE_PREFIX_PATH', spec['adios2'].prefix)
        if spec.satisfies("+hdf5"):
            env.prepend_path('CMAKE_PREFIX_PATH', spec['hdf5'].prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # pre-load dependent CMake-PUBLIC header-only libs
        env.prepend_path('CMAKE_PREFIX_PATH',
                         self.spec['mpark-variant'].prefix)
        env.prepend_path('CPATH', self.spec['mpark-variant'].prefix.include)
