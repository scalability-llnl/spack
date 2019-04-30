# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Faodel(CMakePackage):
    """Flexible, Asynchronous, Object Data-Exchange Libraries"""

    homepage = "https://github.com/faodel/faodel"
    url      = "https://github.com/faodel/faodel/archive/v1.1811.1.tar.gz"
    git      = "https://github.com/faodel/faodel.git"

    maintainers = ['fbudin69500', 'chuckatkins']

    version('develop', branch='master')
    version('1.1811.1', sha256='8e95ee99b8c136ff687eb07a2481ee04560cb1526408eb22ab56cd9c60206916')
    version('1.1803.1', sha256='70ce7125c02601e14abe5985243d67adf677ed9e7a4dd6d3eaef8a97cf281a16')

    variant('shared', default=False,
            description='Build Faodel as shared libs')
    variant('mpi', default=True,
            description='Enable MPI')
    variant('hdf5', default=False, description="Build the HDF5-based IOM in Kelpie")

    variant('tcmalloc', default=True,
            description='Use tcmalloc from gperftools in Lunasa, \
                         potentially other places')
    variant('logging', default='stdout', values=('stdout', 'sbl', 'disabled'),
            description='Select where logging interface output is routed')
    variant('network', default='nnti', values=('nnti', 'libfabric'),
            description='RDMA Network library to use for \
                         low-level communication')

    depends_on('mpi', when='+mpi')
    depends_on('boost+mpi', when='+mpi', type='build')
    depends_on('boost~mpi', when='~mpi', type='build')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('hdf5~mpi', when='+hdf5~mpi')
    depends_on('libfabric', when='network=libfabric')

    # Github issue #11267
    # Requires master branch of `leveldb` which is not available in spack
    # (only versions 1.20 and 1.18 are available).
    # depends_on('leveldb', when='+leveldb')
    # variant('leveldb', default=False,
    #        description='Build the LevelDB-based IOM in Kelpie')

    # FAODEL Github issue #4
    patch('faodel_mpi.patch', when='~mpi')
    # FAODEL Github issue #5
    patch('faodel_sbl.patch', when='logging=sbl')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DBUILD_TESTS:BOOL=OFF',
            '-DBOOST_ROOT:PATH={0}'.format(spec['boost'].prefix),
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
                spec.variants['network'].value)
        ]
        return args
