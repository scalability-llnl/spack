# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Faodel(CMakePackage):
    """Flexible, Asynchronous, Object Data-Exchange Libraries"""

    homepage = "https://github.com/faodel/faodel"
    url      = "https://github.com/faodel/faodel/archive/v1.1906.1.tar.gz"
    git      = "https://github.com/faodel/faodel.git"

    maintainers = ['tkordenbrock', 'craigulmer']

    version('master', branch='master')
    version('1.1906.1', sha256='4b3caf469ae7db50e9bb8d652e4cb532d33d474279def0f8a483f69385648058')
    version('1.1811.2', sha256='22feb502dad0f56fb8af492f6e2cdc53a97fd6c31f6fa3c655be0a6266c46996')
    version('1.1811.1', sha256='8e95ee99b8c136ff687eb07a2481ee04560cb1526408eb22ab56cd9c60206916')
    version('1.1803.1', sha256='70ce7125c02601e14abe5985243d67adf677ed9e7a4dd6d3eaef8a97cf281a16')

    variant('shared',   default=True,  description='Build Faodel as shared libs')
    variant('mpi',      default=True,  description='Enable MPI')

    variant('cereal',   default=False, description='Use Cereal to serialize NNTI data structures else XDR')
    variant('hdf5',     default=False, description="Build the HDF5-based IOM in Kelpie")
    variant('tcmalloc', default=True,  description='Use tcmalloc from gperftools in Lunasa, potentially other places')

    variant('logging', default='stdout', values=('stdout', 'sbl', 'disabled'), description='Select where logging interface output is routed')
    variant('network', default='nnti',   values=('nnti', 'libfabric'),         description='RDMA Network library to use for low-level communication')

    depends_on('mpi', when='+mpi')
    depends_on('boost@1.60.0:')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('cmake@3.8.0:', type='build')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('hdf5~mpi', when='+hdf5~mpi')
    depends_on('libfabric@1.5.3:', when='network=libfabric')
    depends_on('googletest@1.7.0:', type='build')

    # FAODEL requires C++11 support which starts with gcc 4.8.1
    conflicts('%gcc@:4.8.0')

    # Github issue #11267
    # Requires master branch of `leveldb` which is not available in spack
    # (only versions 1.20 and 1.18 are available).
    # depends_on('leveldb', when='+leveldb')
    # variant('leveldb', default=False,
    #        description='Build the LevelDB-based IOM in Kelpie')

    # Only clang requires this patch, but it should be applied for all
    patch('array.patch', when="@1.1803.1")

    # FAODEL Github issue #4
    patch('faodel_mpi.patch', when='@1.1811.1 ~mpi')
    # FAODEL Github issue #5
    patch('faodel_sbl.patch', when='@1.1811.1 logging=sbl')
    patch('lambda-capture-f0267fc.patch', when='@1.1906.1')
    patch('ugni-target-redef-b67e856.patch', when='@1.1906.1')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DBUILD_TESTS:BOOL={0}'.format(
                'ON' if '+mpi' in spec else 'OFF'),
            '-DBOOST_ROOT:PATH={0}'.format(spec['boost'].prefix),
            '-DGTEST_ROOT:PATH={0}'.format(spec['googletest'].prefix),
            '-DBUILD_DOCS:BOOL=OFF',
            '-DFaodel_ENABLE_IOM_HDF5:BOOL={0}'.format(
                'ON' if '+hdf5' in spec else 'OFF'),
            '-DFaodel_ENABLE_IOM_LEVELDB:BOOL={0}'.format(
                'ON' if '+leveldb' in spec else 'OFF'),
            '-DFaodel_ENABLE_MPI_SUPPORT:BOOL={0}'.format(
                'ON' if '+mpi' in spec else 'OFF'),
            '-DFaodel_ENABLE_TCMALLOC:BOOL={0}'.format(
                'ON' if '+tcmalloc' in spec else 'OFF'),
            '-DFaodel_LOGGING_METHOD:STRING={0}'.format(
                spec.variants['logging'].value),
            '-DFaodel_NETWORK_LIBRARY:STRING={0}'.format(
                spec.variants['network'].value),
            '-DFaodel_ENABLE_CEREAL:BOOL={0}'.format(
                'ON' if '+cereal' in spec else 'OFF')
        ]
        return args
