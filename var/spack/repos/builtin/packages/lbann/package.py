# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Lbann(CMakePackage, CudaPackage, ROCmPackage):
    """LBANN: Livermore Big Artificial Neural Network Toolkit.  A distributed
    memory, HPC-optimized, model and data parallel training toolkit for deep
    neural networks.
    """

    homepage = "http://software.llnl.gov/lbann/"
    url      = "https://github.com/LLNL/lbann/archive/v0.91.tar.gz"
    git      = "https://github.com/LLNL/lbann.git"

    maintainers = ['bvanessen']

    version('develop', branch='develop')
    version('0.101', sha256='69d3fe000a88a448dc4f7e263bcb342c34a177bd9744153654528cd86335a1f7')
    version('0.100', sha256='d1bab4fb6f1b80ae83a7286cc536a32830890f6e5b0c3107a17c2600d0796912')
    version('0.99',   sha256='3358d44f1bc894321ce07d733afdf6cb7de39c33e3852d73c9f31f530175b7cd')
    version('0.98.1', sha256='9a2da8f41cd8bf17d1845edf9de6d60f781204ebd37bffba96d8872036c10c66')
    version('0.98',   sha256='8d64b9ac0f1d60db553efa4e657f5ea87e790afe65336117267e9c7ae6f68239')
    version('0.97.1', sha256='2f2756126ac8bb993202cf532d72c4d4044e877f4d52de9fdf70d0babd500ce4')
    version('0.97',   sha256='9794a706fc7ac151926231efdf74564c39fbaa99edca4acb745ee7d20c32dae7')
    version('0.96', sha256='97af78e9d3c405e963361d0db96ee5425ee0766fa52b43c75b8a5670d48e4b4a')
    version('0.95', sha256='d310b986948b5ee2bedec36383a7fe79403721c8dc2663a280676b4e431f83c2')
    version('0.94', sha256='567e99b488ebe6294933c98a212281bffd5220fc13a0a5cd8441f9a3761ceccf')
    version('0.93', sha256='77bfd7fe52ee7495050f49bcdd0e353ba1730e3ad15042c678faa5eeed55fb8c')
    version('0.92', sha256='9187c5bcbc562c2828fe619d53884ab80afb1bcd627a817edb935b80affe7b84')
    version('0.91', sha256='b69f470829f434f266119a33695592f74802cff4b76b37022db00ab32de322f5')

    variant('al', default=True, description='Builds with support for Aluminum Library')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))
    variant('conduit', default=True,
            description='Builds with support for Conduit Library '
            '(note that for v0.99 conduit is required)')
    variant('deterministic', default=False,
            description='Builds with support for deterministic execution')
    variant('dihydrogen', default=True,
            description='Builds with support for DiHydrogen Tensor Library')
    variant('distconv', default=False,
            description='Builds with support for spatial, filter, or channel '
            'distributed convolutions')
    variant('docs', default=False, description='Builds with support for building documentation')
    variant('dtype', default='float',
            description='Type for floating point representation of weights',
            values=('float', 'double'))
    variant('extras', default=False, description='Add python modules for LBANN related tools')
    variant('fft', default=False, description='Support for FFT operations')
    variant('half', default=False,
            description='Builds with support for FP16 precision data types')
    variant('hwloc', default=True, description='Add support for topology aware algorithms')
    variant('nvprof', default=False, description='Build with region annotations for NVPROF')
    variant('numpy', default=False,
            description='Builds with support for processing NumPy data files')
    variant('vision', default=False,
            description='Builds with support for image processing data with OpenCV')
    variant('vtune', default=False, description='Builds with support for Intel VTune')
    variant('onednn', default=False, description='Support for OneDNN')
    variant('nvshmem', default=False, description='Support for NVSHMEM')
    variant('python', default=True, description='Support for Python extensions (e.g. Data Reader)')
    variant('pfe', default=True, description='Python Frontend for generating and launching models')
    variant('boost', default=False, description='Enable callbacks that use Boost libraries')

    # Variant Conflicts
    conflicts('@:0.90,0.99:', when='~conduit')
    conflicts('@0.90:0.101.99', when='+fft')
    conflicts('@:0.90,0.101.99:', when='~dihydrogen')
    conflicts('~cuda', when='+nvprof')
    conflicts('~hwloc', when='+al')
    conflicts('~cuda', when='+nvshmem')
    conflicts('+cuda', when='+rocm', msg='CUDA and ROCm support are mutually exclusive')
    conflicts('+extras', when='~pfe', msg='Python extras require the Python front end support')

    conflicts('~vision', when='@0.91:0.101')
    conflicts('~numpy', when='@0.91:0.101')
    conflicts('~python', when='@0.91:0.101')
    conflicts('~pfe', when='@0.91:0.101')

    depends_on('cmake@3.17.0:', type='build')

    # Specify the correct versions of Hydrogen
    depends_on('hydrogen@:1.3.4', when='@0.95:0.100')
    depends_on('hydrogen@1.4.0:1.4.99', when='@0.101:0.101.99')
    depends_on('hydrogen@1.5.0:', when='@:0.90,0.102:')

    # Add Hydrogen variants
    depends_on('hydrogen +openmp +openmp_blas +shared +int64')
    depends_on('hydrogen ~al', when='~al')
    depends_on('hydrogen +al', when='+al')
    depends_on('hydrogen ~cuda', when='~cuda')
    depends_on('hydrogen +cuda', when='+cuda')
    depends_on('hydrogen ~half', when='~half')
    depends_on('hydrogen +half', when='+half')
    depends_on('hydrogen ~rocm', when='~rocm')
    depends_on('hydrogen +rocm', when='+rocm')
    depends_on('hydrogen build_type=Debug', when='build_type=Debug')

    # Older versions depended on Elemental not Hydrogen
    depends_on('elemental +openmp_blas +shared +int64', when='@0.91:0.94')
    depends_on('elemental +openmp_blas +shared +int64 build_type=Debug',
               when='build_type=Debug @0.91:0.94')

    # Specify the correct version of Aluminum
    depends_on('aluminum@:0.3.99', when='@0.95:0.100 +al')
    depends_on('aluminum@0.4:0.4.99', when='@0.101:0.101.99 +al')
    depends_on('aluminum@0.5.0:', when='@:0.90,0.102: +al')

    # Add Aluminum variants
    depends_on('aluminum +cuda +nccl +ht +cuda_rma', when='+al +cuda')
    depends_on('aluminum +rocm +rccl +ht', when='+al +rocm')

    depends_on('dihydrogen@0.2.0:', when='@:0.90,0.102:')
    depends_on('dihydrogen +openmp', when='+dihydrogen')
    depends_on('dihydrogen ~cuda', when='+dihydrogen ~cuda')
    depends_on('dihydrogen +cuda', when='+dihydrogen +cuda')
    depends_on('dihydrogen ~al', when='+dihydrogen ~al')
    depends_on('dihydrogen +al', when='+dihydrogen +al')
    depends_on('dihydrogen +distconv +cuda', when='+distconv')
    depends_on('dihydrogen ~half', when='+dihydrogen ~half')
    depends_on('dihydrogen +half', when='+dihydrogen +half')
    depends_on('dihydrogen ~nvshmem', when='+dihydrogen ~nvshmem')
    depends_on('dihydrogen +nvshmem', when='+dihydrogen +nvshmem')
    depends_on('dihydrogen ~rocm', when='+dihydrogen ~rocm')
    depends_on('dihydrogen +rocm', when='+dihydrogen +rocm')
    depends_on('dihydrogen@0.1', when='@0.101:0.101.99 +dihydrogen')
    depends_on('dihydrogen@:0.0,0.2:', when='@:0.90,0.102: +dihydrogen')
    conflicts('~dihydrogen', when='+distconv')

    for arch in CudaPackage.cuda_arch_values:
        depends_on('hydrogen cuda_arch=%s' % arch, when='+cuda cuda_arch=%s' % arch)
        depends_on('aluminum cuda_arch=%s' % arch, when='+al +cuda cuda_arch=%s' % arch)
        depends_on('dihydrogen cuda_arch=%s' % arch, when='+dihydrogen +cuda cuda_arch=%s' % arch)
        depends_on('nccl cuda_arch=%s' % arch, when='+cuda cuda_arch=%s' % arch)

    # variants +rocm and amdgpu_targets are not automatically passed to
    # dependencies, so do it manually.
    for val in ROCmPackage.amdgpu_targets:
        depends_on('hydrogen amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)
        depends_on('aluminum amdgpu_target=%s' % val, when='+al amdgpu_target=%s' % val)
        depends_on('dihydrogen amdgpu_target=%s' % val, when='+dihydrogen amdgpu_target=%s' % val)

    depends_on('cudnn', when='@0.90:0.100.99 +cuda')
    depends_on('cudnn@8.0.2:', when='@:0.90,0.101: +cuda')
    depends_on('cub', when='@0.94:0.98.2 +cuda ^cuda@:10.99')
    depends_on('hipcub', when='+rocm')
    depends_on('mpi')
    depends_on('hwloc@1.11:', when='@:0.90,0.102: +hwloc')
    depends_on('hwloc@1.11:1.11.99', when='@0.95:0.101.99 +hwloc')
    depends_on('hwloc +cuda +nvml', when='+cuda')
    depends_on('hwloc@2.3.0:', when='+rocm')

    depends_on('half', when='+half')

    depends_on('fftw@3.3: +openmp', when='+fft')

    # LBANN wraps OpenCV calls in OpenMP parallel loops, build without OpenMP
    # Additionally disable video related options, they incorrectly link in a
    # bad OpenMP library when building with clang or Intel compilers
    depends_on('opencv@4.1.0: build_type=RelWithDebInfo +core +highgui '
               '+imgcodecs +imgproc +jpeg +png +tiff +fast-math ~cuda',
               when='+vision')

    # Note that for Power systems we want the environment to add  +powerpc
    depends_on('opencv@4.1.0: +powerpc', when='+vision arch=ppc64le:')

    depends_on('cnpy', when='+numpy')
    depends_on('nccl', when='@0.94:0.98.2 +cuda')

    depends_on('conduit@0.4.0: +hdf5~hdf5_compat', when='@0.94:0.99 +conduit')
    depends_on('conduit@0.5.0:0.6.99 +hdf5~hdf5_compat', when='@0.100:0.101 +conduit')
    depends_on('conduit@0.6.0: +hdf5~hdf5_compat', when='@:0.90,0.99:')

    # LBANN can use Python in two modes 1) as part of an extensible framework
    # and 2) to drive the front end model creation and launch

    # Core library support for Python Data Reader and extensible interface
    depends_on('python@3: +shared', type=('run'), when='@:0.90,0.99: +python')
    extends("python", when='+python')

    # Python front end and possible extra packages
    depends_on('python@3: +shared', type=('build', 'run'), when='@:0.90,0.99: +pfe')
    extends("python", when='+pfe')
    depends_on('py-setuptools', type='build', when='+pfe')
    depends_on('py-argparse', type='run', when='@:0.90,0.99: +pfe ^python@:2.6')
    depends_on('py-configparser', type='run', when='@:0.90,0.99: +pfe +extras')
    depends_on('py-graphviz@0.10.1:', type='run', when='@:0.90,0.99: +pfe +extras')
    depends_on('py-matplotlib@3.0.0:', type='run', when='@:0.90,0.99: +pfe +extras')
    depends_on('py-numpy@1.16.0:', type=('build', 'run'), when='@:0.90,0.99: +pfe +extras')
    depends_on('py-onnx@1.3.0:', type='run', when='@:0.90,0.99: +pfe +extras')
    depends_on('py-pandas@0.24.1:', type='run', when='@:0.90,0.99: +pfe +extras')
    depends_on('py-texttable@1.4.0:', type='run', when='@:0.90,0.99: +pfe +extras')
    depends_on('py-pytest', type='test', when='@:0.90,0.99: +pfe')
    depends_on('py-protobuf+cpp@3.10.0', type=('build', 'run'), when='@:0.90,0.99: +pfe')

    depends_on('protobuf+shared@3.10.0', when='@:0.90,0.99:')

    depends_on('py-breathe', type='build', when='+docs')
    depends_on('doxygen', type='build', when='+docs')
    depends_on('py-m2r', type='build', when='+docs')

    depends_on('cereal')
    depends_on('catch2', type=('build', 'test'))
    depends_on('clara')

    depends_on('llvm-openmp', when='%apple-clang')

    depends_on('onednn cpu_runtime=omp gpu_runtime=none', when='+onednn')
    depends_on('nvshmem', when='+nvshmem')

    depends_on('zstr')

    generator = 'Ninja'
    depends_on('ninja', type='build')

    @property
    def common_config_args(self):
        spec = self.spec
        # Environment variables
        cppflags = []
        cppflags.append('-DLBANN_SET_EL_RNG')
        args = []
        args.extend([
            '-DCMAKE_CXX_FLAGS=%s' % ' '.join(cppflags),
            '-DLBANN_VERSION=spack',
        ])

        if '+numpy' in spec:
            args.append(
                '-DCNPY_DIR={0}'.format(spec['cnpy'].prefix),
            )

        return args

    def setup_build_environment(self, env):
        if self.spec.satisfies('%apple-clang'):
            env.append_flags(
                'CPPFLAGS', self.compiler.openmp_flag)
            env.append_flags(
                'CFLAGS', self.spec['llvm-openmp'].headers.include_flags)
            env.append_flags(
                'CXXFLAGS', self.spec['llvm-openmp'].headers.include_flags)
            env.append_flags(
                'LDFLAGS', self.spec['llvm-openmp'].libs.ld_flags)

    # Get any recent versions or non-numeric version
    # Note that develop > numeric and non-develop < numeric

    @when('@:0.90,0.94:')
    def cmake_args(self):
        spec = self.spec
        args = self.common_config_args
        args.extend([
            '-DCMAKE_CXX_STANDARD=17',
            '-DLBANN_WITH_CNPY=%s' % ('+numpy' in spec),
            '-DLBANN_DETERMINISTIC:BOOL=%s' % ('+deterministic' in spec),
            '-DLBANN_WITH_HWLOC=%s' % ('+hwloc' in spec),
            '-DLBANN_WITH_ALUMINUM:BOOL=%s' % ('+al' in spec),
            '-DLBANN_WITH_BOOST:BOOL=%s' % ('+boost' in spec),
            '-DLBANN_WITH_CONDUIT:BOOL=%s' % ('+conduit' in spec),
            '-DLBANN_WITH_NVSHMEM:BOOL=%s' % ('+nvshmem' in spec),
            '-DLBANN_WITH_FFT:BOOL=%s' % ('+fft' in spec),
            '-DLBANN_WITH_ONEDNN:BOOL=%s' % ('+onednn' in spec),
            '-DLBANN_WITH_EMBEDDED_PYTHON:BOOL=%s' % ('+python' in spec),
            '-DLBANN_WITH_PYTHON_FRONTEND:BOOL=%s' % ('+pfe' in spec),
            '-DLBANN_WITH_TBINF=OFF',
            '-DLBANN_WITH_UNIT_TESTING:BOOL=%s' % (self.run_tests),
            '-DLBANN_WITH_VISION:BOOL=%s' % ('+vision' in spec),
            '-DLBANN_WITH_VTUNE:BOOL=%s' % ('+vtune' in spec),
            '-DLBANN_DATATYPE={0}'.format(spec.variants['dtype'].value),
            '-DCEREAL_DIR={0}'.format(spec['cereal'].prefix),
            # protobuf is included by py-protobuf+cpp
            '-DProtobuf_DIR={0}'.format(spec['protobuf'].prefix),
            '-Dprotobuf_MODULE_COMPATIBLE=ON'])

        if '+cuda' in spec:
            if spec.satisfies('^cuda@11.0:'):
                args.append('-DCMAKE_CUDA_STANDARD=17')
            else:
                args.append('-DCMAKE_CUDA_STANDARD=14')

        if spec.satisfies('@:0.90') or spec.satisfies('@0.95:'):
            args.append(
                '-DHydrogen_DIR={0}/CMake/hydrogen'.format(
                    spec['hydrogen'].prefix))
        elif spec.satisfies('@0.94'):
            args.append(
                '-DElemental_DIR={0}/CMake/elemental'.format(
                    spec['elemental'].prefix))

        if spec.satisfies('@0.94:0.98.2'):
            args.append('-DLBANN_WITH_NCCL:BOOL=%s' %
                        ('+cuda +nccl' in spec))

        if '+vtune' in spec:
            args.append('-DVTUNE_DIR={0}'.format(spec['vtune'].prefix))

        if '+al' in spec:
            args.append('-DAluminum_DIR={0}'.format(spec['aluminum'].prefix))

        if '+conduit' in spec:
            args.append('-DConduit_DIR={0}'.format(spec['conduit'].prefix))

        # Add support for OpenMP with external (Brew) clang
        if spec.satisfies('%clang platform=darwin'):
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            args.extend([
                '-DOpenMP_CXX_FLAGS=-fopenmp=libomp',
                '-DOpenMP_CXX_LIB_NAMES=libomp',
                '-DOpenMP_libomp_LIBRARY={0}/lib/libomp.dylib'.format(
                    clang_root)])

        if '+vision' in spec:
            args.append('-DOpenCV_DIR:STRING={0}'.format(
                spec['opencv'].prefix))

        if '+cuda' in spec:
            args.append(
                '-DCUDA_TOOLKIT_ROOT_DIR={0}'.format(
                    spec['cuda'].prefix))
            args.append(
                '-DcuDNN_DIR={0}'.format(
                    spec['cudnn'].prefix))
            if spec.satisfies('@0.94:0.98.2'):
                if spec.satisfies('^cuda@:10.99'):
                    args.append('-DCUB_DIR={0}'.format(
                        spec['cub'].prefix))
                if '+nccl' in spec:
                    args.append(
                        '-DNCCL_DIR={0}'.format(
                            spec['nccl'].prefix))
            args.append(
                '-DLBANN_WITH_NVPROF:BOOL=%s' % ('+nvprof' in spec))

        if spec.satisfies('@:0.90') or spec.satisfies('@0.100:'):
            args.append(
                '-DLBANN_WITH_DIHYDROGEN:BOOL=%s' % ('+dihydrogen' in spec))

        if spec.satisfies('@:0.90') or spec.satisfies('@0.101:'):
            args.append(
                '-DLBANN_WITH_DISTCONV:BOOL=%s' % ('+distconv' in spec))

        if '+rocm' in spec:
            args.extend([
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix),
                '-DHIP_CXX_COMPILER={0}'.format(self.spec['hip'].hipcc)])
            archs = self.spec.variants['amdgpu_target'].value
            if archs != 'none':
                arch_str = ",".join(archs)
                cxxflags_str = " ".join(self.spec.compiler_flags['cxxflags'])
                args.append(
                    '-DHIP_HIPCC_FLAGS=--amdgpu-target={0}'
                    ' -g -fsized-deallocation -fPIC -std=c++17 {1}'.format(
                        arch_str, cxxflags_str)
                )

        return args

    @when('@0.91:0.93')
    def cmake_args(self):
        spec = self.spec
        args = self.common_config_args
        args.extend([
            '-DWITH_CUDA:BOOL=%s' % ('+cuda' in spec),
            '-DWITH_CUDNN:BOOL=%s' % ('+cuda' in spec),
            '-DELEMENTAL_USE_CUBLAS:BOOL=%s' % (
                '+cublas' in spec['elemental']),
            '-DWITH_TBINF=OFF',
            '-DWITH_VTUNE=OFF',
            '-DElemental_DIR={0}'.format(spec['elemental'].prefix),
            '-DELEMENTAL_MATH_LIBS={0}'.format(
                spec['elemental'].libs),
            '-DVERBOSE=0',
            '-DLBANN_HOME=.'])

        if spec.variants['dtype'].value == 'float':
            args.append('-DDATATYPE=4')
        elif spec.variants['dtype'].value == 'double':
            args.append('-DDATATYPE=8')

        if '+vision' in spec:
            args.append('-DOpenCV_DIR:STRING={0}'.format(
                spec['opencv'].prefix))

        if '+cudnn' in spec:
            args.append('-DcuDNN_DIR={0}'.format(
                spec['cudnn'].prefix))

        if '+cub' in spec and spec.satisfies('^cuda@:10.99'):
            args.append('-DCUB_DIR={0}'.format(
                spec['cub'].prefix))

        return args
