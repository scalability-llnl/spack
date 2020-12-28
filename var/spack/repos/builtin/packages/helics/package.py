# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Helics(CMakePackage):
    """HELICS is a general-purpose, modular, highly-scalable co-simulation
    framework that runs cross-platform (Linux, Windows, and Mac OS X) and
    supports both event driven and time series simulation."""

    homepage = "https://github.com/GMLC-TDC/HELICS"
    url      = "https://github.com/GMLC-TDC/HELICS/releases/download/v2.4.1/Helics-v2.4.1-source.tar.gz"
    git      = "https://github.com/GMLC-TDC/HELICS.git"

    maintainers = ['nightlark']

    version('develop', branch='develop', submodules=True)
    version('master', branch='master', submodules=True)
    version('2.6.1', sha256='4b9a733a568ae8e6492f93abcd43f1aa9c53b233edcbeb0ab188dcc0d73ac928')
    version('2.6.0', sha256='450cbfc0c37b77ea051d3edc12bbc0f7cf4c1a17091ae10df5214b6176eebb42')
    version('2.5.2', sha256='81928f7e30233a07ae2bfe6c5489fdd958364c0549b2a3e6fdc6163d4b390311')
    version('2.5.1', sha256='3fc3507f7c074ff8b6a17fe54676334158fb2ff7cc8e7f4df011938f28fdbbca')
    version('2.5.0', sha256='6f4f9308ebb59d82d71cf068e0d9d66b6edfa7792d61d54f0a61bf20dd2a7428')
    version('2.4.2', sha256='957856f06ed6d622f05dfe53df7768bba8fe2336d841252f5fac8345070fa5cb')
    version('2.4.1', sha256='ac077e9efe466881ea366721cb31fb37ea0e72a881a717323ba4f3cdda338be4')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('apps', default=True, description="Install the HELICS apps")
    variant('benchmarks', default=False, description="Install the HELICS benchmarks")
    variant('c_shared', default=True, description="Install the C shared library")
    variant('cxx_shared', default=True, description="Install the CXX shared library")
    variant('zmq', default=True, description="Enable ZeroMQ core types")
    variant('tcp', default=True, description="Enable TCP core types")
    variant('udp', default=True, description="Enable UDP core type")
    variant('ipc', default=True, description="Enable IPC core type")
    variant('inproc', default=True, description="Enable in-process core type")
    variant('mpi', default=False, description="Enable MPI core type")
    variant('boost', default=True, description="Compile with Boost libraries")
    variant('asio', default=True, description="Compile with ASIO libraries")
    variant('swig', default=False, description="Build language bindings with SWIG")
    variant('webserver', default=True, description="Enable the integrated webserver in the HELICS broker server")
    variant('python', default=False, description="Enable Python interface")

    # Build dependency
    depends_on('git', type='build', when='@master:')
    depends_on('cmake@3.4:', type='build')
    depends_on('boost@1.70:', type='build', when='+boost')
    depends_on('swig@3.0:', type='build', when='+swig')

    depends_on('libzmq@4.3:', when='+zmq')
    depends_on('mpi@2', when='+mpi')
    depends_on('python@3:', when='+python')

    # OpenMPI doesn't work with HELICS <=2.4.1
    conflicts('^openmpi', when='@:2.4.1 +mpi')

    # Boost is required for ipc and webserver options
    conflicts('+ipc', when='~boost')
    conflicts('+webserver', when='~boost')

    # ASIO (vendored in HELICS repo) is required for tcp and udp options
    conflicts('+tcp', when='~asio')
    conflicts('+udp', when='~asio')

    extends('python', when='+python')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DHELICS_BUILD_EXAMPLES=OFF',
            '-DHELICS_BUILD_TESTS=OFF',
        ]

        # HELICS core type CMake options
        args.append('-DENABLE_ZMQ_CORE={0}'.format(
            'ON' if '+zmq' in spec else 'OFF'))
        args.append('-DENABLE_TCP_CORE={0}'.format(
            'ON' if '+tcp' in spec else 'OFF'))
        args.append('-DENABLE_UDP_CORE={0}'.format(
            'ON' if '+udp' in spec else 'OFF'))
        args.append('-DENABLE_IPC_CORE={0}'.format(
            'ON' if '+ipc' in spec else 'OFF'))
        args.append('-DENABLE_INPROC_CORE={0}'.format(
            'ON' if '+inproc' in spec else 'OFF'))
        args.append('-DENABLE_MPI_CORE={0}'.format(
            'ON' if '+mpi' in spec else 'OFF'))

        # HELICS shared library options
        args.append('-DHELICS_DISABLE_C_SHARED_LIB={0}'.format(
            'OFF' if '+c_shared' in spec else 'ON'))
        args.append('-DHELICS_BUILD_CXX_SHARED_LIB={0}'.format(
            'ON' if '+cxx_shared' in spec else 'OFF'))

        # HELICS executable app options
        args.append('-DHELICS_BUILD_APP_EXECUTABLES={0}'.format(
            'ON' if '+apps' in spec else 'OFF'))
        args.append('-DHELICS_DISABLE_WEBSERVER={0}'.format(
            'OFF' if '+webserver' in spec else 'ON'))
        args.append('-DHELICS_BUILD_BENCHMARKS={0}'.format(
            'ON' if '+benchmarks' in spec else 'OFF'))

        # Extra HELICS library dependencies
        args.append('-DHELICS_DISABLE_BOOST={0}'.format(
            'OFF' if '+boost' in spec else 'ON'))
        args.append('-DHELICS_DISABLE_ASIO={0}'.format(
            'OFF' if '+asio' in spec else 'ON'))

        # SWIG
        args.append('-DHELICS_ENABLE_SWIG={0}'.format(
            'ON' if '+swig' in spec else 'OFF'))

        # Python
        args.append('-DBUILD_PYTHON_INTERFACE={0}'.format(
            'ON' if '+python' in spec else 'OFF'))

        return args

    def setup_run_environment(self, env):
        spec = self.spec
        if '+python' in spec:
            env.prepend_path('PYTHONPATH', self.prefix.python)
