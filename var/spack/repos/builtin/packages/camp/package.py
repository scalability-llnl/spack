# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Camp(CMakePackage, CudaPackage):
    """
    Compiler agnostic metaprogramming library providing concepts,
    type operations and tuples for C++ and cuda
    """

    homepage = "https://github.com/LLNL/camp"
    git      = "https://github.com/LLNL/camp.git"
    url      = "https://github.com/LLNL/camp/archive/v0.1.0.tar.gz"

    version('master', branch='master', submodules='True')
    version('0.1.0', sha256='fd4f0f2a60b82a12a1d9f943f8893dc6fe770db493f8fae5ef6f7d0c439bebcc')

    depends_on('cmake@3.8:', type='build')
    depends_on('cmake@3.9:', type='build', when="+cuda")

    variant('hip', default=False, description='Enable HIP support')

    # possible amd gpu targets for hip builds
    # TODO: we should add a hip build system description equivalent to
    # lib/spack/spack/build_systems/cuda.py, where possible hip amd gpu
    # architectures are defined in a similar way as for cuda gpu
    # architectures. In the meantime, require users to define
    # amd gpu type for hip builds with a variant here.
    amdgpu_targets = (
        'gfx701', 'gfx801', 'gfx802', 'gfx803',
        'gfx900', 'gfx906', 'gfx908', 'gfx1010',
        'gfx1011', 'gfx1012', 'none'
    )
    variant('amdgpu_target', default='none', values=amdgpu_targets)

    depends_on('llvm-amdgpu', when='+hip')
    depends_on('hip', when='+hip')

    # need amd gpu type for hip builds
    conflicts('amdgpu_target=none', when='+hip')

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=ON',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                options.append('-DCMAKE_CUDA_FLAGS:STRING={0}'.format(flag))
        else:
            options.append('-DENABLE_CUDA=OFF')

        if '+hip' in spec:
            arch = self.spec.variants['amdgpu_target'].value
            options.extend([
                '-DENABLE_HIP=ON',
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix),
                '-DHIP_HCC_FLAGS=--amdgpu-target={0}'.format(arch)])
        else:
            options.append('-DENABLE_HIP=OFF')

        options.append('-DENABLE_TESTS={0}'.format(
            "On" if self.run_tests else "Off"))

        return options
