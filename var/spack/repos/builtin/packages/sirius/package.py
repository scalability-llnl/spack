# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    maintainers = ['simonpintarelli', 'haampie', 'dev-zero', 'AdhocMan']

    version('develop', branch='develop')
    version('master', branch='master')

    version('7.2.1', sha256='01bf6c9893ff471473e13351ca7fdc2ed6c1f4b1bb7afa151909ea7cd6fa0de7')
    version('7.2.0', sha256='537800459db8a7553d7aa251c19f3a31f911930194b068bc5bca2dfb2c9b71db')
    version('7.0.2', sha256='ee613607ce3be0b2c3f69b560b2415ce1b0e015179002aa90739430dbfaa0389')
    version('7.0.1', sha256='cca11433f86e7f4921f7956d6589f27bf0fd5539f3e8f96e66a3a6f274888595')
    version('7.0.0', sha256='da783df11e7b65668e29ba8d55c8a6827e2216ad6d88040f84f42ac20fd1bb99')
    version('6.5.7', sha256='d886c3066163c43666ebac2ea50351df03907b5686671e514a75f131ba51b43c',
            preferred=True)
    version('6.5.6', sha256='c8120100bde4477545eae489ea7f9140d264a3f88696ec92728616d78f214cae')
    version('6.5.5', sha256='0b23d3a8512682eea67aec57271031c65f465b61853a165015b38f7477651dd1')
    version('6.5.4', sha256='5f731926b882a567d117afa5e0ed33291f1db887fce52f371ba51f014209b85d')
    version('6.5.3', sha256='eae0c303f332425a8c792d4455dca62557931b28a5df8b4c242652d5ffddd580')
    version('6.5.2', sha256='c18adc45b069ebae03f94eeeeed031ee99b3d8171fa6ee73c7c6fb1e42397fe7')
    version('6.5.1', sha256='599dd0fa25a4e83db2a359257a125e855d4259188cf5b0065b8e7e66378eacf3')
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

    amdgpu_targets = (
        'gfx701', 'gfx801', 'gfx802', 'gfx803',
        'gfx900', 'gfx906', 'gfx908', 'gfx1010',
        'gfx1011', 'gfx1012'
    )

    variant('shared', default=True, description="Build shared libraries")
    variant('openmp', default=True, description="Build with OpenMP support")
    variant('boost_filesystem', default=False,
            description="Use Boost filesystem for self-consistent field method "
                        "mini-app. Only required when the compiler does not "
                        "support std::experimental::filesystem nor std::filesystem")
    variant('fortran', default=False, description="Build Fortran bindings")
    variant('python', default=False, description="Build Python bindings")
    variant('memory_pool', default=True, description="Build with memory pool")
    variant('elpa', default=False, description="Use ELPA")
    variant('vdwxc', default=False, description="Enable libvdwxc support")
    variant('scalapack', default=False, description="Enable scalapack support")
    variant('magma', default=False, description="Enable MAGMA support")
    variant('nlcglib', default=False, description="enable robust wave function optimization")
    variant('rocm', default=False, description='Use ROCm GPU support')
    variant('amdgpu_target', default='gfx803,gfx900,gfx906', multi=True, values=amdgpu_targets)
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo'))
    variant('apps', default=True, description="Build applications")
    variant('tests', default=False, description="Build tests")

    depends_on('python', type=('build', 'run'))
    depends_on('mpi')
    depends_on('gsl')
    depends_on('lapack')
    depends_on('fftw-api@3')
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
    depends_on('boost cxxstd=14 +filesystem', when='+boost_filesystem')

    depends_on('spfft', when='@6.4.0:')
    depends_on('spfft+cuda', when='@6.4.0:+cuda')
    depends_on('spfft+rocm', when='@6.4.0:+rocm')

    depends_on('spla@1.2.0:', when='@7.0.0:')
    depends_on('spla+cuda', when='@7.0.0:+cuda')
    depends_on('spla+rocm', when='@7.0.0:+rocm')

    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')

    depends_on('nlcglib', when='+nlcglib')

    depends_on('libvdwxc+mpi', when='+vdwxc')

    depends_on('scalapack', when='+scalapack')

    # rocm
    depends_on('hip', when='+rocm')
    depends_on('hsakmt-roct', when='+rocm', type='link')
    depends_on('hsa-rocr-dev', when='+rocm', type='link')
    depends_on('rocblas', when='+rocm')

    # FindHIP cmake script only works for < 4.1
    depends_on('hip@:4.0', when='@:7.2.0 +rocm')

    extends('python', when='+python')

    conflicts('+shared', when='@6.3.0:6.4.999')
    conflicts('+boost_filesystem', when='~apps')
    conflicts('^libxc@5.0.0')  # known to produce incorrect results

    # TODO:
    # add support for CRAY_LIBSCI, testing

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
                shared='+shared' in self.spec, recursive=True
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

        args = [
            self.define_from_variant('USE_OPENMP', 'openmp'),
            self.define_from_variant('USE_ELPA', 'elpa'),
            self.define_from_variant('USE_MAGMA', 'magma'),
            self.define_from_variant('USE_NLCGLIB', 'nlcglib'),
            self.define_from_variant('USE_VDWXC', 'vdwxc'),
            self.define_from_variant('USE_MEMORY_POOL', 'memory_pool'),
            self.define_from_variant('USE_SCALAPACK', 'scalapack'),
            self.define_from_variant('CREATE_FORTRAN_BINDINGS', 'fortran'),
            self.define_from_variant('CREATE_PYTHON_MODULE', 'python'),
            self.define_from_variant('USE_CUDA', 'cuda'),
            self.define_from_variant('USE_ROCM', 'rocm'),
            self.define_from_variant('BUILD_TESTING', 'tests'),
            self.define_from_variant('BUILD_APPS', 'apps'),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared')
        ]

        lapack = spec['lapack']
        blas = spec['blas']

        args.extend([
            self.define('LAPACK_FOUND', 'true'),
            self.define('LAPACK_LIBRARIES', lapack.libs.joined(';')),
            self.define('BLAS_FOUND', 'true'),
            self.define('BLAS_LIBRARIES', blas.libs.joined(';'))
        ])

        if '+scalapack' in spec:
            args.extend([
                self.define('SCALAPACK_FOUND', 'true'),
                self.define('SCALAPACK_INCLUDE_DIRS',
                            spec['scalapack'].prefix.include),
                self.define('SCALAPACK_LIBRARIES',
                            spec['scalapack'].libs.joined(';'))
            ])

        if spec['blas'].name in ['intel-mkl', 'intel-parallel-studio']:
            args.append(self.define('USE_MKL', 'ON'))

        if '+elpa' in spec:
            elpa_incdir = os.path.join(
                spec['elpa'].headers.directories[0],
                'elpa'
            )
            args.append(self.define('ELPA_INCLUDE_DIR', elpa_incdir))

        if '+cuda' in spec:
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch[0] != 'none':
                # Specify a single arch directly
                if '@:6' in spec:
                    args.append(self.define(
                        'CMAKE_CUDA_FLAGS',
                        '-arch=sm_{0}'.format(cuda_arch[0]))
                    )

                # Make SIRIUS handle it
                else:
                    args.append(self.define('CUDA_ARCH', ';'.join(cuda_arch)))

        if '+rocm' in spec:
            archs = ",".join(self.spec.variants['amdgpu_target'].value)
            args.extend([
                self.define('HIP_ROOT_DIR', spec['hip'].prefix),
                self.define('HIP_HCC_FLAGS', '--amdgpu-target={0}'.format(archs)),
                self.define('HIP_CXX_COMPILER', self.spec['hip'].hipcc)
            ])

        return args
