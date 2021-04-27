# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bart(MakefilePackage, CudaPackage):
    """BART: Toolbox for Computational Magnetic Resonance Imaging"""

    homepage = "https://mrirecon.github.io/bart/"
    url      = "https://github.com/mrirecon/bart/archive/v0.5.00.tar.gz"

    maintainers = ['glennpj']

    version('0.7.00', sha256='a16afc4b632c703d95b5c34e47acd82fafc19f51f9aff442373eecfef08bfc41')
    version('0.6.00', sha256='dbbd33d1e3ed3324fe21f90a3b62cb51765fe369f21df100b46a32004928f18d')
    version('0.5.00', sha256='30eedcda0f0ef3808157542e0d67df5be49ee41e4f41487af5c850632788f643')

    # patch to fix build with MKL
    patch('https://github.com/mrirecon/bart/commit/b62ca4972d5ac41a44217a5c27123c15daae74db.patch',
          sha256='8fd1be181da928448da750b32d45ee6dce7ba6af0424617c4f8d653cf3f05445',
          when='@0.5.00')

    # patch to fix Makefile for openblas and cuda
    patch('Makefile.patch', when='@:0.6.00')
    patch('Makefile-0.7.00.patch', when='@0.7.00:')

    # patch to set path to bart
    patch('bart_path-0.5.00.patch', when='@0.5.00')
    patch('bart_path-0.6.00.patch', when='@0.6.00:')

    depends_on('libpng')
    depends_on('fftw')
    depends_on('blas')
    depends_on('lapack')
    depends_on('py-numpy', type='run')
    depends_on('py-matplotlib', type='run')
    extends('python')

    conflicts('^atlas', msg='BART does not currently support atlas')

    def edit(self, spec, prefix):
        env['PREFIX'] = prefix
        env['FFTW_BASE'] = spec['fftw'].prefix

        if spec['blas'].name == 'openblas':
            env['OPENBLAS'] = '1'

        if '^mkl' in spec:
            env['MKL'] = '1'
            env['MKL_BASE'] = spec['mkl'].prefix.mkl
        else:
            env['BLAS_BASE'] = spec['blas'].prefix

        if '^netlib-lapack+lapacke' not in spec:
            env['NOLAPACKE'] = '1'

        if '+cuda' in spec:
            cuda_arch = self.spec.variants['cuda_arch'].value
            env['CUDA'] = '1'
            env['CUDA_BASE'] = spec['cuda'].prefix
            env['GPUARCH_FLAGS'] = ' '.join(self.cuda_flags(cuda_arch))

    def install(self, spec, prefix):
        python_dir = join_path(prefix,
                               spec['python'].package.site_packages_dir)

        make('install')

        install_tree('scripts', prefix.scripts)
        install_tree('matlab', prefix.matlab)
        install('startup.m', prefix)

        install('python/bart.py', python_dir)
        install('python/cfl.py', python_dir)
        install('python/wslsupport.py', python_dir)

        if '^python@3:' in spec:
            install('python/bartview3.py', join_path(prefix.bin, 'bartview'))
            filter_file(r'#!/usr/bin/python3', '#!/usr/bin/env python',
                        prefix.bin.bartview)
        else:
            install('python/bartview.py', join_path(prefix.bin, 'bartview'))
            filter_file(r'#!/usr/bin/python', '#!/usr/bin/env python',
                        prefix.bin.bartview)

    def setup_run_environment(self, env):
        env.set('TOOLBOX_PATH', self.prefix)
