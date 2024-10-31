# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def try_le(x, y):
    try:
        return int(x) < y
    except ValueError:
        False


class LcFramework(CMakePackage, CudaPackage):
    """a framework for automatically creating high-speed lossless and
    error-bounded lossy data compression and decompression algorithms."""

    homepage = "https://userweb.cs.txstate.edu/~burtscher/LC/"
    url = "https://github.com/robertu94/LC-framework/archive/refs/tags/1.1.1.tar.gz"
    git = "https://github.com/robertu94/LC-framework"

    maintainers("robertu94")

    version("1.2.2", sha256="957c5da99bca4cfe125486c11b4b7dc6e38f9a158261aff3cd545e47ad9894a6")
    version("1.2.1", commit="98102fdaf443c968ab1bea5f006060b1e4f2d0e7")
    version("1.2.0", commit="2d0f39a927c3487551e4f3c786c3799cada1e203")
    version("1.1.2", sha256="5ccbeaf8e2ef93894854406054210c8525055d195b39e2f141b4f81175fe2815")

    depends_on("cxx", type="build")  # generated

    variant("libpressio", description="build a libpressio plugin for LC", default=False)
    conflicts("+cuda", when="@:1.2.1")
    for sm in [i for i in CudaPackage.cuda_arch_values if try_le(i, 60)]:
        conflicts(
            "cuda_arch={sm}".format(sm=sm), when="+cuda", msg="cuda_arch 60 or newer is required"
        )

    depends_on("python", type=("build",))
    depends_on("libpressio@0.98.0:", when="+libpressio")
    depends_on("libpressio+cuda", when="+cuda+libpressio")

    def cmake_args(self):
        args = [self.define_from_variant("LC_BUILD_LIBPRESSIO_PLUGIN", "libpressio")]
        if self.spec.satisfies("+cuda"):
            args.append(self.define_from_variant("LC_BUILD_CUDA", "cuda"))
            args.append(self.builder.define_cuda_architectures(self))

        return args
