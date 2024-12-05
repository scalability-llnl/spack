# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Genomeworks(CMakePackage, CudaPackage):
    """SDK for GPU accelerated genome assembly and analysis."""

    homepage = "https://clara-parabricks.github.io/GenomeWorks/"
    url = "https://github.com/clara-parabricks/GenomeWorks/archive/v0.5.3.tar.gz"
    git = "https://github.com/clara-parabricks/GenomeWorks.git"

    license("Apache-2.0")

    version(
        "0.5.3", tag="v0.5.3", commit="b4b8bf76ea2ce44452d3a1107e66d47968414adb", submodules=True
    )
    version(
        "0.5.2", tag="v0.5.2", commit="d94b6d55a7f9cca8056912ebe9281c77dfc89997", submodules=True
    )
    version(
        "0.5.1", tag="v0.5.1", commit="8cade237403f5ece5b133772232766875f046f20", submodules=True
    )
    version(
        "0.5.0", tag="v0.5.0", commit="3f3837c1a6f8cb6ee4c3d9d177ea38f7c325bf5a", submodules=True
    )
    version(
        "0.4.4", tag="v0.4.4", commit="0cb889061cb4a8c134d96590cc73721601dec283", submodules=True
    )
    version(
        "0.4.3", tag="v0.4.3", commit="97b0b704eee85304602495284343c2135a2ecc22", submodules=True
    )
    version(
        "0.4.0", tag="v0.4.0", commit="fbf7a6a84c8a5681150c864d5180729226bf48d8", submodules=True
    )
    version(
        "0.3.0", tag="v0.3.0", commit="957d4497f8867f1368382c096e2cf7523dd847fb", submodules=True
    )
    version(
        "0.2.0", tag="v0.2.0", commit="416af9f1817a4a70745b3f7cdb7418125159f75c", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.10.2:", type=("build"))
    depends_on("cuda@11:", type=("build", "run"))
    depends_on("python@3.6.7:", type=("build", "run"))

    # Disable CUB compilation, as it is already included in CUDA 11.
    # See https://github.com/clara-parabricks/GenomeWorks/issues/570
    # This patch breaks GenomeWorks with Cuda <11, cuda@11: is
    # therefore used as dependency.
    patch("3rdparty.patch")

    def cmake_args(self):
        args = []
        spec = self.spec
        if spec.satisfies("+cuda"):
            args.append("-DWITH_CUDA=ON")
            args.append("-Dgw_cuda_gen_all_arch=ON")
            args.append("-DTHRUST_IGNORE_CUB_VERSION_CHECK=ON")
            cuda_arch = spec.variants["cuda_arch"].value
            if cuda_arch != "none":
                args.append("-DCUDA_FLAGS=-arch=sm_{0}".format(cuda_arch[0]))
        else:
            args.append("-DWITH_CUDA=OFF")
        return args
