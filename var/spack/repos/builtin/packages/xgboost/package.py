# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xgboost(CMakePackage, CudaPackage):
    """XGBoost is an optimized distributed gradient boosting library designed to be
    highly efficient, flexible and portable. It implements machine learning algorithms
    under the Gradient Boosting framework. XGBoost provides a parallel tree boosting
    (also known as GBDT, GBM) that solve many data science problems in a fast and
    accurate way. The same code runs on major distributed environment (Hadoop, SGE, MPI)
    and can solve problems beyond billions of examples."""

    homepage = "https://xgboost.ai/"
    git      = "https://github.com/dmlc/xgboost.git"

    maintainers = ['adamjstewart']

    version('master', branch='master', submodules=True)
    version('1.3.3', tag='v1.3.3', submodules=True)
    version('0.90', tag='v0.90', submodules=True, deprecated=True)
    version('0.81', tag='v0.81', submodules=True, deprecated=True)

    variant('nccl', default=False, description='Build with NCCL to enable distributed GPU support')
    variant('openmp', default=True, description='Build with OpenMP support')

    depends_on('cmake@3.13:', type='build')
    depends_on('cmake@3.16:', when='platform=darwin', type='build')
    depends_on('ninja', type='build')
    depends_on('cuda@10:', when='+cuda')
    depends_on('nccl', when='+nccl')
    depends_on('llvm-openmp', when='%apple-clang +openmp')

    conflicts('%gcc@:4.999', msg='GCC version must be at least 5.0!')
    conflicts('+nccl', when='~cuda', msg='NCCL requires CUDA')
    conflicts('+cuda', when='~openmp', msg='CUDA requires OpenMP')

    generator = 'Ninja'

    def cmake_args(self):
        # https://xgboost.readthedocs.io/en/latest/build.html
        args = [
            self.define_from_variant('USE_CUDA', 'cuda'),
            self.define_from_variant('USE_NCCL', 'nccl'),
            self.define_from_variant('USE_OPENMP', 'openmp'),
        ]

        if '+cuda' in self.spec and 'cuda_arch=none' not in self.spec:
            args.append(self.define(
                'GPU_COMPUTE_VER', self.spec.variants['cuda_arch'].value))

        return args
