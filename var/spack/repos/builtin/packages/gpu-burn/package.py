# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GpuBurn(MakefilePackage, CudaPackage):
    """Multi-GPU CUDA stress test. Note that the file pointed to by COMPARE_PTX
    needs to be copied or linked to the current working directory before
    running gpu_burn."""

    homepage = "http://wili.cc/blog/gpu-burn.html"
    url      = "http://wili.cc/blog/entries/gpu-burn/gpu_burn-1.0.tar.gz"

    version('1.0', sha256='d55994f0bee8dabf021966dbe574ef52be1e43386faeee91318dd4ebb36aa74a')

    patch('Makefile.patch')

    # This package uses CudaPackage to pick up the cuda_arch variant. A side
    # effect is that it also picks up the cuda variant, but cuda is required
    # for gpu-burn so is not really a variant.
    variant('cuda', 'True', description='Use CUDA; must be true')

    conflicts('~cuda', msg='gpu-burn requires cuda')
    conflicts('cuda_arch=none', msg='must select a CUDA architecture')

    cuda_arch_values = CudaPackage.cuda_arch_values
    variant(
        'cuda_arch',
        description='CUDA architecture',
        default='none',
        values=('none',) + cuda_arch_values,
        multi=False
    )

    def edit(self, spec, prefix):
        # update cuda architecture if necessary
        if '+cuda' in self.spec:
            cuda_arch = self.spec.variants['cuda_arch'].value
            archflag = '-arch=compute_{0}'.format(cuda_arch)
            filter_file('-arch=compute_30', archflag,
                        'Makefile', string=True)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        install('gpu_burn', prefix.bin)
        install('compare.ptx', prefix.share)

    # The gpu_burn program looks for the compare.ptx file in the current
    # working directory. Create an environment variable that can be pointed to
    # so that it can be copied or linked.
    def setup_run_environment(self, env):
        env.set('COMPARE_PTX', join_path(self.prefix.share, 'compare.ptx'))
