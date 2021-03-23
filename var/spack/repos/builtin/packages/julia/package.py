# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Julia(Package):
    """The Julia Language: A fresh approach to technical computing"""

    homepage = "http://julialang.org"
    url      = "https://github.com/JuliaLang/julia/releases/download/v0.4.3/julia-0.4.3-full.tar.gz"
    git      = "https://github.com/JuliaLang/julia.git"

    maintainers = ['glennpj']

    version('master', branch='master')
    version('1.5.3', sha256='fb69337ca037576758547c7eed9ae8f153a9c052318327b6b7f1917408c14d91')
    version('1.5.2', sha256='850aed3fe39057488ec633f29af705f5ada87e3058fd65e48ad26f91b713a19a')
    version('1.5.1', sha256='1d0debfccfc7cd07047aa862dd2b1a96f7438932da1f5feff6c1033a63f9b1d4')
    version('1.5.0', sha256='4a6ffadc8dd04ca0b7fdef6ae203d0af38185e57b78f7c0b972c4707354a6d1b')
    version('1.4.2', sha256='948c70801d5cce81eeb7f764b51b4bfbb2dc0b1b9effc2cb9fc8f8cf6c90a334')
    version('1.4.1', sha256='b21585db55673ac0668c163678fcf2aad11eb7c64bb2aa03a43046115fab1553')
    version('1.4.0', sha256='880c73a08296ce8d94ad9605149f2a2b2b028e7202a700ef725da899300b8be9')
    version('1.3.1', sha256='053908ec2706eb76cfdc998c077de123ecb1c60c945b4b5057aa3be19147b723')
    version('1.2.0', sha256='2419b268fc5c3666dd9aeb554815fe7cf9e0e7265bc9b94a43957c31a68d9184')
    version('1.1.1', sha256='3c5395dd3419ebb82d57bcc49dc729df3b225b9094e74376f8c649ee35ed79c2')
    version('1.0.0', sha256='1a2497977b1d43bb821a5b7475b4054b29938baae8170881c6b8dd4099d133f1')
    version('0.6.2', sha256='1e34c13091c9ddb47cf87a51566d94a06613f3db3c483b8f63b276e416dd621b')
    version('0.5.2', sha256='f5ef56d79ed55eacba9fe968bb175317be3f61668ef93e747d76607678cc01dd')
    version('0.5.1', sha256='533b6427a1b01bd38ea0601f58a32d15bf403f491b8415e9ce4305b8bc83bb21')
    version('0.5.0', sha256='732478536b6dccecbf56e541eef0aed04de0e6d63ae631b136e033dda2e418a9')
    version('0.4.7', sha256='d658d5bd5fb79b19f3c01cadb9aba8622ca8a12a4b687acc7d99c21413623570')
    version('0.4.6', sha256='4c23c9fc72398014bd39327c2f7efd3a301884567d4cb2a89105c984d4d633ba')
    version('0.4.5', sha256='cbf361c23a77e7647040e8070371691083e92aa93c8a318afcc495ad1c3a71d9')
    version('0.4.3', sha256='2b9df25a8f58df8e43038ec30bae195dfb160abdf925f3fa193b59d40e4113c5')

    variant('cxx', default=False, description='Prepare for Julia Cxx package')
    variant('mkl', default=False, description='Use Intel MKL')

    patch('gc.patch', when='@0.4:0.4.5')
    patch('openblas.patch', when='@0.4:0.4.5')
    patch('armgcc.patch', when='@1.0.0:1.1.1 %gcc@:5.9 target=aarch64:')

    # Build-time dependencies:
    # depends_on('awk')
    depends_on('m4', type='build')
    # depends_on('pkgconfig')
    # Python only needed to build LLVM?
    depends_on('python@2.7:2.8', type='build', when='@:1.1')
    depends_on('python@2.7:', type='build', when='@1.2:')
    depends_on('cmake@2.8:', type='build', when='@1.0:')
    depends_on('cmake@:3.11', type='build', when='@:1.4')
    depends_on('git', type='build', when='@master')

    # Combined build-time and run-time dependencies:
    # (Yes, these are run-time dependencies used by Julia's package manager.)
    depends_on('cmake @2.8:', type=('build', 'run'), when='@:0.6')
    depends_on('curl', when='@:0.5.0')
    depends_on('git', type=('build', 'run'), when='@:0.4')
    depends_on('openssl@:1.0', when='@:0.5.0')
    depends_on('mkl', when='+mkl')

    # Run-time dependencies:
    # depends_on('arpack')
    # depends_on('fftw +float')
    # depends_on('gmp')
    # depends_on('libgit')
    # depends_on('mpfr')
    # depends_on('openblas')
    # depends_on('pcre2')

    # ARPACK: Requires BLAS and LAPACK; needs to use the same version
    # as Julia.

    # BLAS and LAPACK: Julia prefers 64-bit versions on 64-bit
    # systems. OpenBLAS has an option for this; make it available as
    # variant.

    # FFTW: Something doesn't work when using a pre-installed FFTW
    # library; need to investigate.

    # GMP, MPFR: Something doesn't work when using a pre-installed
    # FFTW library; need to investigate.

    # LLVM: Julia works only with specific versions, and might require
    # patches. Thus we let Julia install its own LLVM.

    # Other possible dependencies:
    # USE_SYSTEM_OPENLIBM=0
    # USE_SYSTEM_OPENSPECFUN=0
    # USE_SYSTEM_DSFMT=0
    # USE_SYSTEM_SUITESPARSE=0
    # USE_SYSTEM_UTF8PROC=0
    # USE_SYSTEM_LIBGIT2=0

    conflicts('+cxx', when='@:0.6', msg='Variant cxx requires Julia >= 1.0.0')

    conflicts('@:0.7.0', when='target=aarch64:')

    # GCC conflicts
    conflicts('@:0.5.1', when='%gcc@8:', msg='Julia <= 0.5.1 needs GCC <= 7')

    # Building recent versions of Julia with Intel is untested and unsupported
    # by the Julia project, https://github.com/JuliaLang/julia/issues/23407.
    conflicts('@0.6:', when='%intel',
              msg='Only Julia <= 0.5.x can be built with the Intel compiler.')
    conflicts('%intel', when='~mkl',
              msg='Building with the Intel compiler requires the mkl variant '
              '(+mkl)')

    def setup_build_environment(self, env):
        # The julia build can have trouble with finding GCC libraries with the
        # spack compiler.
        if self.compiler.name == 'gcc':
            gcc_base = os.path.split(os.path.split(self.compiler.cc)[0])[0]
            env.prepend_path('LD_LIBRARY_PATH', join_path(gcc_base, 'lib64'))

    def install(self, spec, prefix):
        # Julia needs git tags
        if os.path.isfile('.git/shallow'):
            git = which('git')
            git('fetch', '--unshallow')
        # Explicitly setting CC, CXX, or FC breaks building libuv, one
        # of Julia's dependencies. This might be a Darwin-specific
        # problem. Given how Spack sets up compilers, Julia should
        # still use Spack's compilers, even if we don't specify them
        # explicitly. Potential options are
        # 'CC=cc',
        # 'CXX=c++',
        # 'FC=fc',
        # 'USE_SYSTEM_ARPACK=1',
        # 'override USE_SYSTEM_CURL=1',
        # 'USE_SYSTEM_FFTW=1',
        # 'USE_SYSTEM_GMP=1',
        # 'USE_SYSTEM_MPFR=1',
        # 'USE_SYSTEM_PCRE=1',
        options = [
            'prefix={0}'.format(prefix)
        ]
        if '@:0.5.0' in spec:
            options += [
                'override USE_SYSTEM_CURL=1'
            ]

        if '+cxx' in spec:
            options += [
                'BUILD_LLVM_CLANG=1',
                'LLVM_ASSERTIONS=1',
                'USE_LLVM_SHLIB=1'
            ]
        if spec.target.family == 'aarch64':
            options += [
                'JULIA_CPU_TARGET=generic',
                'MARCH=armv8-a+crc'
            ]

        if spec.target.family == 'x86_64' or spec.target.family == 'x86':
            if spec.target == 'x86_64':
                options += [
                    'JULIA_CPU_TARGET=generic'
                ]
            else:
                target_str = str(spec.target).replace('_', '-')
                if target_str == "zen2":
                    target_str = "znver2"
                options += [
                    'JULIA_CPU_TARGET={0}'.format(target_str)
                ]

        if '%intel' in spec:
            options += [
                'USEICC=1',
                'USEIFC=1',
                'USE_INTEL_LIBM=1'
            ]

        if '+mkl' in spec:
            options += [
                'USE_INTEL_MKL=1',
            ]
        with open('Make.user', 'w') as f:
            f.write('\n'.join(options) + '\n')

        make()
        make('install')

        # Julia's package manager needs a certificate
        if '@:0.5.0' in spec:
            cacert_dir = join_path(prefix, 'etc', 'curl')
            mkdirp(cacert_dir)
            cacert_file = join_path(cacert_dir, 'cacert.pem')
            curl = which('curl')
            curl('--create-dirs',
                 '--output', cacert_file,
                 'https://curl.haxx.se/ca/cacert.pem')
