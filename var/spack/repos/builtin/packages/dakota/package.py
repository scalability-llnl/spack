# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dakota(CMakePackage):
    """The Dakota toolkit provides a flexible, extensible interface between
    analysis codes and iterative systems analysis methods. Dakota
    contains algorithms for:

    - optimization with gradient and non gradient-based methods;
    - uncertainty quantification with sampling, reliability, stochastic
    - expansion, and epistemic methods;
    - parameter estimation with nonlinear least squares methods;
    - sensitivity/variance analysis with design of experiments and
    - parameter study methods.

    These capabilities may be used on their own or as components within
    advanced strategies such as hybrid optimization, surrogate-based
    optimization, mixed integer nonlinear programming, or optimization
    under uncertainty.

    """

    homepage = 'https://dakota.sandia.gov/'
    url = 'https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.12-release-public.src.tar.gz'

    version('6.13', sha256='bca9448ebbcc5a29226eab2abbd9e5e87ccaef6818658edb64588f234bf7bd1b')
    version('6.12', sha256='4d69f9cbb0c7319384ab9df27643ff6767eb410823930b8fbd56cc9de0885bc9')
    version('6.11', sha256='d38bbfccba4ff5f2187bdbb45633e269ef4d9f68631a17a52b4d05b5f9b75f65')
    version('6.10', sha256='2a0d2f426c0f369cfa3c0b341061553e651a6f60377a59f83251d9d3c3821bad')
    version('6.9', sha256='ede7149843707f4b07e76aae27e6a6826734131938da8a6c1b7ed11865c7ee84')
    version('6.8', sha256='43dc6027b7f666478f2aff7663803463cef98ab2269a55f69c02ada861659c24')
    version('6.3', sha256='0fbc310105860d77bb5c96de0e8813d75441fca1a5e6dfaf732aa095c4488d52', url='https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.3-public.src.tar.gz')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('mpi', default=True, description='Activates MPI support')
    variant('hdf5', default=False, description='Activate HDF5 support')

    # Generic 'lapack' provider won't work, dakota searches for
    # 'LAPACKConfig.cmake' or 'lapack-config.cmake' on the path
    depends_on('netlib-lapack')

    depends_on('blas')
    depends_on('mpi', when='+mpi')
    depends_on('python@3:', when='@6.8:')
    depends_on('python@:2', when='@:6.8')

    # Build fails with boost > 1.68.0.
    depends_on('boost@:1.68.0')
    depends_on('cmake@2.8.9:', type='build')
    depends_on('hdf5', when='+hdf5')

    conflicts('+mpi', when='@:6.3',
              msg='Dakota <= 6.3 cannot be built with MPI, '
                  'please disable the MPI variant.')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),

            'DAKOTA_HAVE_HDF5:BOOL=%s' % (
                'ON' if '+hdf5' in spec else 'OFF'),
        ]

        if '+mpi' in spec:
            args.extend([
                '-DDAKOTA_HAVE_MPI:BOOL=ON',
                '-DMPI_CXX_COMPILER:STRING=%s' % join_path(spec['mpi'].mpicxx),
            ])

        return args
