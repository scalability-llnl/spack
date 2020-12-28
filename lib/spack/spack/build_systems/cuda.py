# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_base import PackageBase
from spack.directives import depends_on, variant, conflicts

import spack.variant


class CudaPackage(PackageBase):
    """Auxiliary class which contains CUDA variant, dependencies and conflicts
    and is meant to unify and facilitate its usage.

    Maintainers: ax3l, Rombur
    """

    # https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#gpu-feature-list
    # https://developer.nvidia.com/cuda-gpus
    # https://en.wikipedia.org/wiki/CUDA#GPUs_supported
    cuda_arch_values = (
        '10', '11', '12', '13',
        '20', '21',
        '30', '32', '35', '37',
        '50', '52', '53',
        '60', '61', '62',
        '70', '72', '75',
        '80', '86'
    )

    # FIXME: keep cuda and cuda_arch separate to make usage easier until
    # Spack has depends_on(cuda, when='cuda_arch!=None') or alike
    variant('cuda', default=False,
            description='Build with CUDA')

    variant('cuda_arch',
            description='CUDA architecture',
            values=spack.variant.any_combination_of(*cuda_arch_values))

    # https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#nvcc-examples
    # https://llvm.org/docs/CompileCudaWithLLVM.html#compiling-cuda-code
    @staticmethod
    def cuda_flags(arch_list):
        return [('--generate-code arch=compute_{0},code=sm_{0} '
                 '--generate-code arch=compute_{0},code=compute_{0}').format(s)
                for s in arch_list]

    depends_on('cuda', when='+cuda')

    # CUDA version vs Architecture
    # https://en.wikipedia.org/wiki/CUDA#GPUs_supported
    # https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#deprecated-features
    depends_on('cuda@:6.0',     when='cuda_arch=10')
    depends_on('cuda@:6.5',     when='cuda_arch=11')
    depends_on('cuda@2.1:6.5',  when='cuda_arch=12')
    depends_on('cuda@2.1:6.5',  when='cuda_arch=13')

    depends_on('cuda@3.0:8.0',  when='cuda_arch=20')
    depends_on('cuda@3.2:8.0',  when='cuda_arch=21')

    depends_on('cuda@5.0:10.2', when='cuda_arch=30')
    depends_on('cuda@5.0:10.2', when='cuda_arch=32')
    depends_on('cuda@5.0:',     when='cuda_arch=35')
    depends_on('cuda@6.5:',     when='cuda_arch=37')

    depends_on('cuda@6.0:',     when='cuda_arch=50')
    depends_on('cuda@6.5:',     when='cuda_arch=52')
    depends_on('cuda@6.5:',     when='cuda_arch=53')

    depends_on('cuda@8.0:',     when='cuda_arch=60')
    depends_on('cuda@8.0:',     when='cuda_arch=61')
    depends_on('cuda@8.0:',     when='cuda_arch=62')

    depends_on('cuda@9.0:',     when='cuda_arch=70')
    depends_on('cuda@9.0:',     when='cuda_arch=72')
    depends_on('cuda@10.0:',    when='cuda_arch=75')

    depends_on('cuda@11.0:',    when='cuda_arch=80')
    depends_on('cuda@11.1:',    when='cuda_arch=86')

    # There are at least three cases to be aware of for compiler conflicts
    # 1. Linux x86_64
    # 2. Linux ppc64le
    # 3. Mac OS X
    # CUDA-compiler conflicts are version-to-version specific and are
    # difficult to express with the current Spack conflict syntax

    # Linux x86_64 compiler conflicts from here:
    # https://gist.github.com/ax3l/9489132
    arch_platform = ' target=x86_64: platform=linux'
    conflicts('%gcc@5:', when='+cuda ^cuda@:7.5' + arch_platform)
    conflicts('%gcc@6:', when='+cuda ^cuda@:8' + arch_platform)
    conflicts('%gcc@7:', when='+cuda ^cuda@:9.1' + arch_platform)
    conflicts('%gcc@8:', when='+cuda ^cuda@:10.0.130' + arch_platform)
    conflicts('%gcc@9:', when='+cuda ^cuda@:10.2.89' + arch_platform)
    conflicts('%gcc@:4', when='+cuda ^cuda@11.0.2:' + arch_platform)
    conflicts('%gcc@10:', when='+cuda ^cuda@:11.0.2' + arch_platform)
    conflicts('%gcc@11:', when='+cuda ^cuda@:11.1.0' + arch_platform)
    conflicts('%pgi@:14.8', when='+cuda ^cuda@:7.0.27' + arch_platform)
    conflicts('%pgi@:15.3,15.5:', when='+cuda ^cuda@7.5' + arch_platform)
    conflicts('%pgi@:16.2,16.0:16.3', when='+cuda ^cuda@8' + arch_platform)
    conflicts('%pgi@:15,18:', when='+cuda ^cuda@9.0:9.1' + arch_platform)
    conflicts('%pgi@:16,19:', when='+cuda ^cuda@9.2.88:10' + arch_platform)
    conflicts('%pgi@:17,20:',
              when='+cuda ^cuda@10.1.105:10.2.89' + arch_platform)
    conflicts('%pgi@:17,21:',
              when='+cuda ^cuda@11.0.2:11.1.0' + arch_platform)
    conflicts('%clang@:3.4', when='+cuda ^cuda@:7.5' + arch_platform)
    conflicts('%clang@:3.7,4:',
              when='+cuda ^cuda@8.0:9.0' + arch_platform)
    conflicts('%clang@:3.7,4.1:',
              when='+cuda ^cuda@9.1' + arch_platform)
    conflicts('%clang@:3.7,5.1:', when='+cuda ^cuda@9.2' + arch_platform)
    conflicts('%clang@:3.7,6.1:', when='+cuda ^cuda@10.0.130' + arch_platform)
    conflicts('%clang@:3.7,7.1:', when='+cuda ^cuda@10.1.105' + arch_platform)
    conflicts('%clang@:3.7,8.1:',
              when='+cuda ^cuda@10.1.105:10.1.243' + arch_platform)
    conflicts('%clang@:3.2,9:', when='+cuda ^cuda@10.2.89' + arch_platform)
    conflicts('%clang@:5', when='+cuda ^cuda@11.0.2:' + arch_platform)
    conflicts('%clang@10:', when='+cuda ^cuda@:11.0.2' + arch_platform)
    conflicts('%clang@11:', when='+cuda ^cuda@:11.1.0' + arch_platform)

    # x86_64 vs. ppc64le differ according to NVidia docs
    # Linux ppc64le compiler conflicts from Table from the docs below:
    # https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html
    # https://docs.nvidia.com/cuda/archive/9.2/cuda-installation-guide-linux/index.html
    # https://docs.nvidia.com/cuda/archive/9.1/cuda-installation-guide-linux/index.html
    # https://docs.nvidia.com/cuda/archive/9.0/cuda-installation-guide-linux/index.html
    # https://docs.nvidia.com/cuda/archive/8.0/cuda-installation-guide-linux/index.html

    arch_platform = ' target=ppc64le: platform=linux'
    # information prior to CUDA 9 difficult to find
    conflicts('%gcc@6:', when='+cuda ^cuda@:9' + arch_platform)
    conflicts('%gcc@8:', when='+cuda ^cuda@:10.0.130' + arch_platform)
    conflicts('%gcc@9:', when='+cuda ^cuda@:10.1.243' + arch_platform)
    # officially, CUDA 11.0.2 only supports the system GCC 8.3 on ppc64le
    conflicts('%gcc@:4', when='+cuda ^cuda@11.0.2:' + arch_platform)
    conflicts('%gcc@10:', when='+cuda ^cuda@:11.0.2' + arch_platform)
    conflicts('%gcc@11:', when='+cuda ^cuda@:11.1.0' + arch_platform)
    conflicts('%pgi', when='+cuda ^cuda@:8' + arch_platform)
    conflicts('%pgi@:16', when='+cuda ^cuda@:9.1.185' + arch_platform)
    conflicts('%pgi@:17', when='+cuda ^cuda@:10' + arch_platform)
    conflicts('%clang@4:', when='+cuda ^cuda@:9.0.176' + arch_platform)
    conflicts('%clang@5:', when='+cuda ^cuda@:9.1' + arch_platform)
    conflicts('%clang@6:', when='+cuda ^cuda@:9.2' + arch_platform)
    conflicts('%clang@7:', when='+cuda ^cuda@10.0.130' + arch_platform)
    conflicts('%clang@7.1:', when='+cuda ^cuda@:10.1.105' + arch_platform)
    conflicts('%clang@8.1:', when='+cuda ^cuda@:10.2.89' + arch_platform)
    conflicts('%clang@:5', when='+cuda ^cuda@11.0.2:' + arch_platform)
    conflicts('%clang@10:', when='+cuda ^cuda@:11.0.2' + arch_platform)
    conflicts('%clang@11:', when='+cuda ^cuda@:11.1.0' + arch_platform)

    # Intel is mostly relevant for x86_64 Linux, even though it also
    # exists for Mac OS X. No information prior to CUDA 3.2 or Intel 11.1
    conflicts('%intel@:11.0', when='+cuda ^cuda@:3.1')
    conflicts('%intel@:12.0', when='+cuda ^cuda@5.5:')
    conflicts('%intel@:13.0', when='+cuda ^cuda@6.0:')
    conflicts('%intel@:13.2', when='+cuda ^cuda@6.5:')
    conflicts('%intel@:14.9', when='+cuda ^cuda@7:')
    # Intel 15.x is compatible with CUDA 7 thru current CUDA
    conflicts('%intel@16.0:', when='+cuda ^cuda@:8.0.43')
    conflicts('%intel@17.0:', when='+cuda ^cuda@:8.0.60')
    conflicts('%intel@18.0:', when='+cuda ^cuda@:9.9')
    conflicts('%intel@19.0:', when='+cuda ^cuda@:10.0')
    conflicts('%intel@19.1:', when='+cuda ^cuda@:10.1')
    conflicts('%intel@19.2:', when='+cuda ^cuda@:11.1.0')

    # XL is mostly relevant for ppc64le Linux
    conflicts('%xl@:12,14:', when='+cuda ^cuda@:9.1')
    conflicts('%xl@:12,14:15,17:', when='+cuda ^cuda@9.2')
    conflicts('%xl@:12,17:', when='+cuda ^cuda@:11.1.0')

    # Mac OS X
    # platform = ' platform=darwin'
    # Apple XCode clang vs. LLVM clang are difficult to specify
    # with spack syntax. Xcode clang name is `clang@x.y.z-apple`
    # which precludes ranges being specified. We have proposed
    # rename XCode clang to `clang@apple-x.y.z` or even
    # `clang-apple@x.y.z as a possible fix.
    # Compiler conflicts will be eventual taken from here:
    # https://docs.nvidia.com/cuda/cuda-installation-guide-mac-os-x/index.html#abstract
    conflicts('platform=darwin', when='+cuda ^cuda@11.0.2:')

    # Make sure cuda_arch can not be used without +cuda
    for value in cuda_arch_values:
        conflicts('~cuda', when='cuda_arch=' + value)
