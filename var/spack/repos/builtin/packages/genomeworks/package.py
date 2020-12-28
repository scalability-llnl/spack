# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Genomeworks(CMakePackage, CudaPackage):
    """SDK for GPU accelerated genome assembly and analysis."""

    homepage = "https://clara-parabricks.github.io/GenomeWorks/"
    url      = "https://github.com/clara-parabricks/GenomeWorks/archive/v0.5.3.tar.gz"
    git      = "https://github.com/clara-parabricks/GenomeWorks.git"

    version('0.5.3', tag='v0.5.3', submodules=True)
    version('0.5.2', tag='v0.5.2', submodules=True)
    version('0.5.1', tag='v0.5.1', submodules=True)
    version('0.5.0', tag='v0.5.0', submodules=True)
    version('0.4.4', tag='v0.4.4', submodules=True)
    version('0.4.3', tag='v0.4.3', submodules=True)
    version('0.4.0', tag='v0.4.0', submodules=True)
    version('0.3.0', tag='v0.3.0', submodules=True)
    version('0.2.0', tag='v0.2.0', submodules=True)

    depends_on('cmake@3.10.2:', type=('build'))
    depends_on('cuda@11:', type=('build', 'run'))
    depends_on('python@3.6.7:', type=('build', 'run'))

    # Disable CUB compilation, as it is already included in CUDA 11.
    # See https://github.com/clara-parabricks/GenomeWorks/issues/570
    # This patch breaks GenomeWorks with Cuda <11, cuda@11: is
    # therefore used as dependency.
    patch('3rdparty.patch')

    def cmake_args(self):
        args = []
        spec = self.spec
        if '+cuda' in spec:
            args.append('-DWITH_CUDA=ON')
            args.append('-Dgw_cuda_gen_all_arch=ON')
            args.append('-DTHRUST_IGNORE_CUB_VERSION_CHECK=ON')
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch != 'none':
                args.append('-DCUDA_FLAGS=-arch=sm_{0}'.format(cuda_arch[0]))
        else:
            args.append('-DWITH_CUDA=OFF')
        return args
