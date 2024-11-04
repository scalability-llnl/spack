# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
from typing import Iterable, List

import spack.variant
from spack.directives import conflicts, depends_on, variant
from spack.multimethod import when
from spack.package_base import PackageBase


class CudaPackage(PackageBase):
    """Auxiliary class which contains CUDA variant, dependencies and conflicts
    and is meant to unify and facilitate its usage.

    Maintainers: ax3l, Rombur, davidbeckingsale
    """

    # https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#gpu-feature-list
    # https://developer.nvidia.com/cuda-gpus
    # https://en.wikipedia.org/wiki/CUDA#GPUs_supported
    cuda_arch_values = (
        "10",
        "11",
        "12",
        "13",
        "20",
        "21",
        "30",
        "32",
        "35",
        "37",
        "50",
        "52",
        "53",
        "60",
        "61",
        "62",
        "70",
        "72",
        "75",
        "80",
        "86",
        "87",
        "89",
        "90",
        "90a",
    )

    # FIXME: keep cuda and cuda_arch separate to make usage easier until
    # Spack has depends_on(cuda, when='cuda_arch!=None') or alike
    variant("cuda", default=False, description="Build with CUDA")

    variant(
        "cuda_arch",
        description="CUDA architecture",
        values=spack.variant.any_combination_of(*cuda_arch_values),
        sticky=True,
        when="+cuda",
    )

    # https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#nvcc-examples
    # https://llvm.org/docs/CompileCudaWithLLVM.html#compiling-cuda-code
    @staticmethod
    def cuda_flags(arch_list):
        return [
            (
                "--generate-code arch=compute_{0},code=sm_{0} "
                "--generate-code arch=compute_{0},code=compute_{0}"
            ).format(s)
            for s in arch_list
        ]

    @staticmethod
    def compute_capabilities(arch_list: Iterable[str]) -> List[str]:
        """Adds a decimal place to each CUDA arch.

        >>> compute_capabilities(['90', '90a'])
        ['9.0', '9.0a']

        Args:
            arch_list: A list of integer strings, optionally followed by a suffix.

        Returns:
            A list of float strings, optionally followed by a suffix
        """
        pattern = re.compile(r"(\d+)")
        capabilities = []
        for arch in arch_list:
            _, number, letter = re.split(pattern, arch)
            number = "{0:.1f}".format(float(number) / 10.0)
            capabilities.append(number + letter)
        return capabilities

    depends_on("cuda", when="+cuda")

    # CUDA version vs Architecture
    # https://en.wikipedia.org/wiki/CUDA#GPUs_supported
    # https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#deprecated-features
    depends_on("cuda@:6.0", when="cuda_arch=10")
    depends_on("cuda@:6.5", when="cuda_arch=11")
    depends_on("cuda@2.1:6.5", when="cuda_arch=12")
    depends_on("cuda@2.1:6.5", when="cuda_arch=13")

    depends_on("cuda@3.0:8.0", when="cuda_arch=20")
    depends_on("cuda@3.2:8.0", when="cuda_arch=21")

    depends_on("cuda@5.0:10.2", when="cuda_arch=30")
    depends_on("cuda@5.0:10.2", when="cuda_arch=32")
    depends_on("cuda@5.0:11.8", when="cuda_arch=35")
    depends_on("cuda@6.5:11.8", when="cuda_arch=37")

    depends_on("cuda@6.0:", when="cuda_arch=50")
    depends_on("cuda@6.5:", when="cuda_arch=52")
    depends_on("cuda@6.5:", when="cuda_arch=53")

    depends_on("cuda@8.0:", when="cuda_arch=60")
    depends_on("cuda@8.0:", when="cuda_arch=61")
    depends_on("cuda@8.0:", when="cuda_arch=62")

    depends_on("cuda@9.0:", when="cuda_arch=70")
    depends_on("cuda@9.0:", when="cuda_arch=72")
    depends_on("cuda@10.0:", when="cuda_arch=75")

    depends_on("cuda@11.0:", when="cuda_arch=80")
    depends_on("cuda@11.1:", when="cuda_arch=86")
    depends_on("cuda@11.4:", when="cuda_arch=87")
    depends_on("cuda@11.8:", when="cuda_arch=89")

    depends_on("cuda@12.0:", when="cuda_arch=90")
    depends_on("cuda@12.0:", when="cuda_arch=90a")

    # From the NVIDIA install guide we know of conflicts for particular
    # platforms (linux, darwin), architectures (x86, powerpc) and compilers
    # (gcc, clang). We don't restrict %gcc and %clang conflicts to
    # platform=linux, since they may apply to platform=darwin. We currently
    # do not provide conflicts for platform=darwin with %apple-clang.

    # Linux x86_64 compiler conflicts from here:
    # https://gist.github.com/ax3l/9489132
    with when("^cuda~allow-unsupported-compilers"):
        # GCC
        # According to
        # https://github.com/spack/spack/pull/25054#issuecomment-886531664
        # these conflicts are valid independently from the architecture

        # minimum supported versions
        conflicts("%gcc@:4", when="+cuda ^cuda@11.0:")
        conflicts("%gcc@:5", when="+cuda ^cuda@11.4:")
        conflicts("%clang@:6", when="+cuda ^cuda@12.2:")

        # maximum supported version
        # NOTE:
        # in order to not constrain future cuda version to old gcc versions,
        # it has been decided to use an upper bound for the latest version.
        # This implies that the last one in the list has to be updated at
        # each release of a new cuda minor version.
        conflicts("%gcc@10:", when="+cuda ^cuda@:11.0")
        conflicts("%gcc@11:", when="+cuda ^cuda@:11.4.0")
        conflicts("%gcc@11.2:", when="+cuda ^cuda@:11.5")
        conflicts("%gcc@12:", when="+cuda ^cuda@:11.8")
        conflicts("%gcc@13:", when="+cuda ^cuda@:12.3")
        conflicts("%gcc@14:", when="+cuda ^cuda@:12.6")
        conflicts("%clang@12:", when="+cuda ^cuda@:11.4.0")
        conflicts("%clang@13:", when="+cuda ^cuda@:11.5")
        conflicts("%clang@14:", when="+cuda ^cuda@:11.7")
        conflicts("%clang@15:", when="+cuda ^cuda@:12.0")
        conflicts("%clang@16:", when="+cuda ^cuda@:12.1")
        conflicts("%clang@17:", when="+cuda ^cuda@:12.3")
        conflicts("%clang@18:", when="+cuda ^cuda@:12.5")
        conflicts("%clang@19:", when="+cuda ^cuda@:12.6")

        # https://gist.github.com/ax3l/9489132#gistcomment-3860114
        conflicts("%gcc@10", when="+cuda ^cuda@:11.4.0")
        conflicts("%gcc@5:", when="+cuda ^cuda@:7.5 target=x86_64:")
        conflicts("%gcc@6:", when="+cuda ^cuda@:8 target=x86_64:")
        conflicts("%gcc@7:", when="+cuda ^cuda@:9.1 target=x86_64:")
        conflicts("%gcc@8:", when="+cuda ^cuda@:10.0.130 target=x86_64:")
        conflicts("%gcc@9:", when="+cuda ^cuda@:10.2.89 target=x86_64:")
        conflicts("%pgi@:14.8", when="+cuda ^cuda@:7.0.27 target=x86_64:")
        conflicts("%pgi@:15.3,15.5:", when="+cuda ^cuda@7.5 target=x86_64:")
        conflicts("%pgi@:16.2,16.0:16.3", when="+cuda ^cuda@8 target=x86_64:")
        conflicts("%pgi@:15,18:", when="+cuda ^cuda@9.0:9.1 target=x86_64:")
        conflicts("%pgi@:16,19:", when="+cuda ^cuda@9.2.88:10.0 target=x86_64:")
        conflicts("%pgi@:17,20:", when="+cuda ^cuda@10.1.105:10.2.89 target=x86_64:")
        conflicts("%pgi@:17,21:", when="+cuda ^cuda@11.0.2:11.1.0 target=x86_64:")
        conflicts("%clang@:3.4", when="+cuda ^cuda@:7.5 target=x86_64:")
        conflicts("%clang@:3.7,4:", when="+cuda ^cuda@8.0:9.0 target=x86_64:")
        conflicts("%clang@:3.7,4.1:", when="+cuda ^cuda@9.1 target=x86_64:")
        conflicts("%clang@:3.7,5.1:", when="+cuda ^cuda@9.2 target=x86_64:")
        conflicts("%clang@:3.7,6.1:", when="+cuda ^cuda@10.0.130 target=x86_64:")
        conflicts("%clang@:3.7,7.1:", when="+cuda ^cuda@10.1.105 target=x86_64:")
        conflicts("%clang@:3.7,8.1:", when="+cuda ^cuda@10.1.105:10.1.243 target=x86_64:")
        conflicts("%clang@:3.2,9:", when="+cuda ^cuda@10.2.89 target=x86_64:")
        conflicts("%clang@:5", when="+cuda ^cuda@11.0.2: target=x86_64:")
        conflicts("%clang@10:", when="+cuda ^cuda@:11.0.3 target=x86_64:")
        conflicts("%clang@11:", when="+cuda ^cuda@:11.1.0 target=x86_64:")

        # x86_64 vs. ppc64le differ according to NVidia docs
        # Linux ppc64le compiler conflicts from Table from the docs below:
        # https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html
        # https://docs.nvidia.com/cuda/archive/9.2/cuda-installation-guide-linux/index.html
        # https://docs.nvidia.com/cuda/archive/9.1/cuda-installation-guide-linux/index.html
        # https://docs.nvidia.com/cuda/archive/9.0/cuda-installation-guide-linux/index.html
        # https://docs.nvidia.com/cuda/archive/8.0/cuda-installation-guide-linux/index.html

        # information prior to CUDA 9 difficult to find
        conflicts("%gcc@6:", when="+cuda ^cuda@:9 target=ppc64le:")
        conflicts("%gcc@8:", when="+cuda ^cuda@:10.0.130 target=ppc64le:")
        conflicts("%gcc@9:", when="+cuda ^cuda@:10.1.243 target=ppc64le:")
        # officially, CUDA 11.0.2 only supports the system GCC 8.3 on ppc64le
        conflicts("%pgi", when="+cuda ^cuda@:8 target=ppc64le:")
        conflicts("%pgi@:16", when="+cuda ^cuda@:9.1.185 target=ppc64le:")
        conflicts("%pgi@:17", when="+cuda ^cuda@:10 target=ppc64le:")
        conflicts("%clang@4:", when="+cuda ^cuda@:9.0.176 target=ppc64le:")
        conflicts("%clang@5:", when="+cuda ^cuda@:9.1 target=ppc64le:")
        conflicts("%clang@6:", when="+cuda ^cuda@:9.2 target=ppc64le:")
        conflicts("%clang@7:", when="+cuda ^cuda@10.0.130 target=ppc64le:")
        conflicts("%clang@7.1:", when="+cuda ^cuda@:10.1.105 target=ppc64le:")
        conflicts("%clang@8.1:", when="+cuda ^cuda@:10.2.89 target=ppc64le:")
        conflicts("%clang@:5", when="+cuda ^cuda@11.0.2: target=ppc64le:")
        conflicts("%clang@10:", when="+cuda ^cuda@:11.0.2 target=ppc64le:")
        conflicts("%clang@11:", when="+cuda ^cuda@:11.1.0 target=ppc64le:")

        # Intel is mostly relevant for x86_64 Linux, even though it also
        # exists for Mac OS X. No information prior to CUDA 3.2 or Intel 11.1
        conflicts("%intel@:11.0", when="+cuda ^cuda@:3.1")
        conflicts("%intel@:12.0", when="+cuda ^cuda@5.5:")
        conflicts("%intel@:13.0", when="+cuda ^cuda@6.0:")
        conflicts("%intel@:13.2", when="+cuda ^cuda@6.5:")
        conflicts("%intel@:14.9", when="+cuda ^cuda@7:")
        # Intel 15.x is compatible with CUDA 7 thru current CUDA
        conflicts("%intel@16.0:", when="+cuda ^cuda@:8.0.43")
        conflicts("%intel@17.0:", when="+cuda ^cuda@:8.0.60")
        conflicts("%intel@18.0:", when="+cuda ^cuda@:9.9")
        conflicts("%intel@19.0:", when="+cuda ^cuda@:10.0")
        conflicts("%intel@19.1:", when="+cuda ^cuda@:10.1")
        conflicts("%intel@19.2:", when="+cuda ^cuda@:11.1.0")
        conflicts("%intel@2021:", when="+cuda ^cuda@:11.4.0")

        # ARM
        # https://github.com/spack/spack/pull/39666#issuecomment-2377609263
        # Might need to be expanded to other gcc versions
        conflicts("%gcc@13.2.0", when="+cuda ^cuda@:12.4 target=aarch64:")

        # XL is mostly relevant for ppc64le Linux
        conflicts("%xl@:12,14:", when="+cuda ^cuda@:9.1")
        conflicts("%xl@:12,14:15,17:", when="+cuda ^cuda@9.2")
        conflicts("%xl@:12,17:", when="+cuda ^cuda@:11.1.0")

        # PowerPC.
        conflicts("target=ppc64le", when="+cuda ^cuda@12.5:")

        # Darwin.
        # TODO: add missing conflicts for %apple-clang cuda@:10
        conflicts("platform=darwin", when="+cuda ^cuda@11.0.2:")
