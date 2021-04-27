# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Casacore(CMakePackage):
    """A suite of c++ libraries for radio astronomy data processing."""

    homepage = "https://github.com/casacore/casacore"
    url      = "https://github.com/casacore/casacore/archive/v2.4.1.tar.gz"

    maintainers = ['mpokorny']

    version('3.4.0', sha256='31f02ad2e26f29bab4a47a2a69e049d7bc511084a0b8263360e6157356f92ae1')
    version('3.3.0', sha256='3a714644b908ef6e81489b792cc9b80f6d8267a275e15d38a42a6a5137d39d3d')
    version('3.2.0', sha256='ae5d3786cb6dfdd7ebc5eecc0c724ff02bbf6929720bc23be43a027978e79a5f')
    version('3.1.2', sha256='ac94f4246412eb45d503f1019cabe2bb04e3861e1f3254b832d9b1164ea5f281')
    version('3.1.1', sha256='85d2b17d856592fb206b17e0a344a29330650a4269c80b87f8abb3eaf3dadad4')
    version('3.1.0', sha256='a6adf2d77ad0d6f32995b1e297fd88d31ded9c3e0bb8f28966d7b35a969f7897')
    version('3.0.0', sha256='6f0e68fd77b5c96299f7583a03a53a90980ec347bff9dfb4c0abb0e2933e6bcb')
    version('2.4.1', sha256='58eccc875053b2c6fe44fe53b6463030ef169597ec29926936f18d27b5087d63')

    depends_on('cmake@3.7.1:', type='build')

    variant('openmp', default=False, description='Build OpenMP support')
    variant('shared', default=True, description='Build shared libraries')
    variant('readline', default=True, description='Build readline support')
    # see note below about the reason for disabling the "sofa" variant
    # variant('sofa', default=False, description='Build SOFA support')
    variant('fftpack', default=False, description='Build FFTPack')
    variant('hdf5', default=False, description='Build HDF5 support')
    variant('python', default=False, description='Build python support')

    # Force dependency on readline in v3.2 and earlier. Although the
    # presence of readline is tested in CMakeLists.txt, and casacore
    # can be built without it, there's no way to control that
    # dependency at build time; since many systems come with readline,
    # it's better to explicitly depend on it here always.
    depends_on('readline', when='@:3.2.0')
    depends_on('readline', when='+readline')
    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('blas')
    depends_on('lapack')
    depends_on('cfitsio')
    depends_on('wcslib@4.20:+cfitsio')
    depends_on('fftw@3.0.0: precision=float,double', when='@3.4.0:')
    depends_on('fftw@3.0.0: precision=float,double', when='~fftpack')
    # SOFA dependency suffers the same problem in CMakeLists.txt as readline;
    # force a dependency when building unit tests
    depends_on('sofa-c', type='test')
    depends_on('hdf5', when='+hdf5')
    depends_on('python@2.6:', when='+python')
    depends_on('boost+python', when='+python')
    depends_on('py-numpy', when='+python')

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append(self.define_from_variant('ENABLE_SHARED', 'shared'))
        args.append(self.define_from_variant('USE_OPENMP', 'openmp'))
        args.append(self.define_from_variant('USE_READLINE', 'readline'))
        args.append(self.define_from_variant('USE_HDF5', 'hdf5'))

        # fftw3 is required by casacore starting with v3.4.0, but the
        # old fftpack is still available. For v3.4.0 and later, we
        # always require FFTW3 dependency with the optional addition
        # of FFTPack. In older casacore versions, only one of FFTW3 or
        # FFTPack can be selected.
        if spec.satisfies('@3.4.0:'):
            if spec.satisfies('+fftpack'):
                args.append('-DBUILD_FFTPACK_DEPRECATED=YES')
            args.append(self.define('USE_FFTW3', True))
        else:
            args.append(self.define('USE_FFTW3', spec.satisfies('~fftpack')))

        # Python2 and Python3 binding
        if spec.satisfies('~python'):
            args.extend(['-DBUILD_PYTHON=NO', '-DBUILD_PYTHON3=NO'])
        elif spec.satisfies('^python@3.0.0:'):
            args.extend(['-DBUILD_PYTHON=NO', '-DBUILD_PYTHON3=YES'])
        else:
            args.extend(['-DBUILD_PYTHON=YES', '-DBUILD_PYTHON3=NO'])

        args.append('-DBUILD_TESTING=OFF')
        return args

    def patch(self):
        # Rely on CMake ability to find hdf5, available since CMake 3.7.X
        os.remove('cmake/FindHDF5.cmake')
