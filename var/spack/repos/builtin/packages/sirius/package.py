# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Sirius(CMakePackage, CudaPackage):
    """Domain specific library for electronic structure calculations"""

    homepage = "https://github.com/electronic-structure/SIRIUS"
    url      = "https://github.com/electronic-structure/SIRIUS/archive/v6.1.5.tar.gz"
    list_url = "https://github.com/electronic-structure/SIRIUS/releases"
    git      = "https://github.com/electronic-structure/SIRIUS.git"

    version('develop', branch='develop')
    version('master', branch='master')

    version('6.5.0', sha256='5544f3abbb71dcd6aa08d18aceaf53c38373de4cbd0c3af44fbb39c20cfeb7cc')
    version('6.4.4', sha256='1c5de9565781847658c3cc11edcb404e6e6d1c5a9dfc81e977de7a9a7a162c8a')
    version('6.4.3', sha256='4d1effeadb84b3e1efd7d9ac88018ef567aa2e0aa72e1112f0abf2e493e2a189')
    version('6.4.2', sha256='40b9b66deebb6538fc0f4cd802554d0d763ea6426b9b2f0e8db8dc617e494479')
    version('6.4.1', sha256='86f25c71517952a63e92e0a9bcf66d27e4afb2b0d67cf84af480f116b8e7f53c')
    version('6.4.0', sha256='bc61758b71dd2996e2ff515b8c3560b2c69c00931cb2811a163a31bcfea4436e')
    version('6.3.4', sha256='8839e988b4bb6ef99b6180f7fba03a5537e31fce51bb3e4c2298b513d6a07e0a')
    version('6.3.3', sha256='7ba30a4e5c9a545433251211454ec0d59b74ba8941346057bc7de11e7f6886f7')
    version('6.3.2', sha256='1723e5ad338dad9a816369a6957101b2cae7214425406b12e8712c82447a7ee5')
    version('6.1.5', sha256='379f0a2e5208fd6d91c2bd4939c3a5c40002975fb97652946fa1bfe4a3ef97cb')

    variant('shared', default=False, description="Build shared libraries")
    variant('openmp', default=True, description="Build with OpenMP support")
    variant('fortran', default=False, description="Build Fortran bindings")
    variant('python', default=False, description="Build Python bindings")
    variant('elpa', default=False, description="Use ELPA")
    variant('vdwxc', default=False, description="Enable libvdwxc support")
    variant('scalapack', default=False, description="Enable scalapack support")
    variant('magma', default=False, description="Enable MAGMA support")
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    depends_on('python', type=('build', 'run'))
    depends_on('mpi')
    depends_on('gsl')
    depends_on('lapack')
    depends_on('fftw')  # SIRIUS does not care about MPI-support in FFTW
    depends_on('libxc')
    depends_on('spglib')
    depends_on('hdf5+hl')
    depends_on('pkgconfig', type='build')
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('py-scipy', when='+python', type=('build', 'run'))
    depends_on('py-h5py', when='+python', type=('build', 'run'))
    depends_on('py-mpi4py', when='+python', type=('build', 'run'))
    depends_on('py-pyyaml', when='+python', type=('build', 'run'))
    depends_on('py-mpi4py', when='+python', type=('build', 'run'))
    depends_on('py-voluptuous', when='+python', type=('build', 'run'))
    depends_on('py-pybind11', when='+python', type=('build', 'run'))
    depends_on('magma', when='+magma')

    depends_on('spfft', when='@6.4.0:')
    depends_on('spfft+cuda', when='@6.4.0:+cuda')
    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    depends_on('libvdwxc+mpi', when='+vdwxc')
    depends_on('scalapack', when='+scalapack')
    depends_on('cuda', when='+cuda')
    extends('python', when='+python')

    conflicts('+shared', when='@6.3.0:')  # option to build shared libraries has been removed

    # TODO:
    # add support for CRAY_LIBSCI, ROCm, testing

    patch("strip-spglib-include-subfolder.patch", when='@6.1.5')
    patch("link-libraries-fortran.patch", when='@6.1.5')
    patch("cmake-fix-shared-library-installation.patch", when='@6.1.5')

    @property
    def libs(self):
        libraries = []

        if '@6.3.0:' in self.spec:
            libraries += ['libsirius']

            return find_libraries(
                libraries, root=self.prefix,
                shared=False, recursive=True
            )

        else:
            if '+fortran' in self.spec:
                libraries += ['libsirius_f']

            if '+cuda' in self.spec:
                libraries += ['libsirius_cu']

            return find_libraries(
                libraries, root=self.prefix,
                shared='+shared' in self.spec, recursive=True
            )

    def cmake_args(self):
        spec = self.spec

        def _def(variant, flag=None):
            """Returns "-DUSE_VARIANT:BOOL={ON,OFF}" depending on whether
               +variant is set. If the CMake flag differs from the variant
               name, pass the flag name explicitly.
            """

            return "-D{0}:BOOL={1}".format(
                flag if flag else "USE_{0}".format(
                    variant.strip('+~').upper()
                ),
                "ON" if variant in spec else "OFF"
            )

        args = [
            _def('+openmp'),
            _def('+elpa'),
            _def('+magma'),
            _def('+vdwxc'),
            _def('+scalapack'),
            _def('+fortran', 'CREATE_FORTRAN_BINDINGS'),
            _def('+python', 'CREATE_PYTHON_MODULE'),
            _def('+cuda')
        ]

        if '@:6.2.999' in self.spec:
            args += [_def('+shared', 'BUILD_SHARED_LIBS')]

        lapack = spec['lapack']
        blas = spec['blas']

        args += [
            '-DLAPACK_FOUND=true',
            '-DLAPACK_LIBRARIES={0}'.format(lapack.libs.joined(';')),
            '-DBLAS_FOUND=true',
            '-DBLAS_LIBRARIES={0}'.format(blas.libs.joined(';')),
        ]

        if '+scalapack' in spec:
            args += [
                '-DSCALAPACK_FOUND=true',
                '-DSCALAPACK_INCLUDE_DIRS={0}'.format(
                    spec['scalapack'].prefix.include),
                '-DSCALAPACK_LIBRARIES={0}'.format(
                    spec['scalapack'].libs.joined(';')),
            ]

        if '^mkl' in spec:
            args += ['-DUSE_MKL=ON']

        if '+elpa' in spec:
            elpa_incdir = os.path.join(
                spec['elpa'].headers.directories[0],
                'elpa'
            )
            args += ["-DELPA_INCLUDE_DIR={0}".format(elpa_incdir)]

        if '+cuda' in spec:
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch[0] != 'none':
                args += [
                    '-DCMAKE_CUDA_FLAGS=-arch=sm_{0}'.format(cuda_arch[0])
                ]

        return args
