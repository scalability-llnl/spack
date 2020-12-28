# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libceed(Package):
    """The CEED API Library: Code for Efficient Extensible Discretizations."""

    homepage = "https://github.com/CEED/libCEED"
    git      = "https://github.com/CEED/libCEED.git"

    maintainers = ['jedbrown', 'v-dobrev', 'tzanio']

    version('develop', branch='main')
    version('0.7', tag='v0.7')
    version('0.6', commit='c7f533e01e2f3f6720fbf37aac2af2ffed225f60')  # tag v0.6 + small portability fixes
    version('0.5', tag='v0.5')
    version('0.4', tag='v0.4')
    version('0.2', tag='v0.2')
    version('0.1', tag='v0.1')

    variant('occa', default=True, description='Enable OCCA backends')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('hip', default=False, description='Enable HIP support')
    variant('debug', default=False, description='Enable debug build')
    variant('libxsmm', default=False, description='Enable LIBXSMM backend')
    variant('magma', default=False, description='Enable MAGMA backend')

    conflicts('+libxsmm', when='@:0.2')
    conflicts('+magma', when='@:0.5')
    conflicts('+hip', when='@:0.6')

    depends_on('cuda', when='+cuda')
    depends_on('hip@3.8.0', when='@0.7:0.7.99+hip')
    depends_on('hip@3.8.0:', when='@0.8:+hip')

    depends_on('occa@develop', when='@develop+occa')
    depends_on('occa@1.1.0', when='@0.7:+occa')
    depends_on('occa@1.0.8:', when='@0.4+occa')
    depends_on('occa@1.0.0-alpha.5,develop', when='@:0.2+occa')
    depends_on('occa+cuda', when='+occa+cuda')
    depends_on('occa~cuda', when='+occa~cuda')

    depends_on('libxsmm', when='+libxsmm')

    depends_on('magma', when='+magma')

    patch('pkgconfig-version-0.4.diff', when='@0.4')

    # occa: do not occaFree kernels
    # Repeated creation and freeing of kernels appears to expose a caching
    # bug in Occa.
    patch('occaFree-0.2.diff', when='@0.2')

    phases = ['build', 'install']

    @property
    def common_make_opts(self):
        spec = self.spec
        compiler = self.compiler
        # Note: The occa package exports OCCA_DIR in the environment

        # Use verbose building output
        makeopts = ['V=1']

        if '@:0.2' in spec:
            makeopts += ['NDEBUG=%s' % ('' if '+debug' in spec else '1')]

        elif '@0.4:' in spec:
            # Determine options based on the compiler:
            if '+debug' in spec:
                opt = '-g'
            elif compiler.name == 'gcc':
                opt = '-O3 -g -ffp-contract=fast'
                if compiler.version >= ver(4.9):
                    opt += ' -fopenmp-simd'
            elif compiler.name == 'apple-clang':
                opt = '-O3 -g -march=native -ffp-contract=fast'
                if compiler.version >= ver(10):
                    opt += ' -fopenmp-simd'
            elif compiler.name == 'clang':
                opt = '-O3 -g -march=native -ffp-contract=fast'
                if compiler.version >= ver(6):
                    opt += ' -fopenmp-simd'
            elif compiler.name in ['xl', 'xl_r']:
                opt = '-O -g -qsimd=auto'
            else:
                opt = '-O -g'
            makeopts += ['OPT=%s' % opt]

            if 'avx' in self.spec.target:
                makeopts.append('AVX=1')

            if '+cuda' in spec:
                makeopts += ['CUDA_DIR=%s' % spec['cuda'].prefix]
                if spec.satisfies('@:0.4'):
                    nvccflags = ['-ccbin %s -Xcompiler "%s" -Xcompiler %s' %
                                 (compiler.cxx, opt, compiler.cc_pic_flag)]
                    nvccflags = ' '.join(nvccflags)
                    makeopts += ['NVCCFLAGS=%s' % nvccflags]
            else:
                # Disable CUDA auto-detection:
                makeopts += ['CUDA_DIR=/disable-cuda']

            if '+hip' in spec:
                makeopts += ['HIP_DIR=%s' % spec['hip'].prefix]

            if '+libxsmm' in spec:
                makeopts += ['XSMM_DIR=%s' % spec['libxsmm'].prefix]

            if '+magma' in spec:
                makeopts += ['MAGMA_DIR=%s' % spec['magma'].prefix]

        return makeopts

    def build(self, spec, prefix):
        makeopts = self.common_make_opts
        make('info', *makeopts)
        make(*makeopts)

        if self.run_tests:
            make('prove', *makeopts, parallel=False)

    def install(self, spec, prefix):
        installopts = ['prefix=%s' % prefix]
        installopts += self.common_make_opts
        make('install', *installopts, parallel=False)

    @when('@0.1')
    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install('ceed.h', prefix.include)
        mkdirp(prefix.lib)
        install('libceed.%s' % dso_suffix, prefix.lib)
        filter_file(r'^prefix=.*$', 'prefix=%s' % prefix, 'ceed.pc')
        filter_file(r'^includedir=\$\{prefix\}$',
                    'includedir=${prefix}/include', 'ceed.pc')
        filter_file(r'^libdir=\$\{prefix\}$',
                    'libdir=${prefix}/lib', 'ceed.pc')
        filter_file(r'Version:.*$', 'Version: 0.1', 'ceed.pc')
        mkdirp(prefix.lib.pkgconfig)
        install('ceed.pc', prefix.lib.pkgconfig)
