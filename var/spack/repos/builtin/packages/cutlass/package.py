# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cutlass(CMakePackage, CudaPackage):
    """CUDA Templates for Linear Algebra Subroutines"""

    homepage = "https://github.com/NVIDIA/cutlass"
    git = homepage + ".git"
    url = "https://github.com/NVIDIA/cutlass/archive/refs/tags/v3.3.0.tar.gz"

    version("main", branch="main")
    version("master", branch="master")
    version("3.4.1", sha256="aebd4f9088bdf2fd640d65835de30788a6c7d3615532fcbdbc626ec3754becd4")
    version("3.4.0", sha256="49f4b854acc2a520126ceefe4f701cfe8c2b039045873e311b1f10a8ca5d5de1")
    version("3.3.0", sha256="99876de94a04d0b9cdee81d4f29659bde1426b416926aef4d9a3a3a7869511a3")
    version("3.2.2", sha256="aaa9719eb806b168695b34893faf4854bb6bc9e09f63f2d36772aaf35a8516e5")
    version("3.2.1", sha256="da4081210d6699a547dbbe3d7cc18b4527df835518a3d0d3c85a373927c3a9b1")
    version("3.2.0", sha256="9637961560a9d63a6bb3f407faf457c7dbc4246d3afb54ac7dc1e014dd7f172f")
    version("3.1.0", sha256="821aa2e5b709a2e5d3922dcf2c5d445b4898a6ef8bac683cfb00125eafbca029")
    version("3.0.0", sha256="ade959981d0937a26c758979dbc97c4df152a511176573ba2d976604de78a3e3")
    version("2.11.0", sha256="b4394f1e080b63cfc54163069334096324c1262dfc66e67099880005d51b8af9")
    version("2.10.0", sha256="8f56727c0c7ca59f67f6904972958a6e7e925f72e112056e6df7bb3fdeacefd7")
    version("2.9.1", sha256="2d6474576c08ee21d7f4f3a10fd1a47234fd9fd638efc8a2e0e64bb367f09bc1")
    version("2.9.0", sha256="ccca4685739a3185e3e518682845314b07a5d4e16d898b10a3c3a490fd742fb4")
    version("2.8.0", sha256="1938f0e739646370a59ba1f5e365be4c701e8d9e0b9b725d306622e9aafa6b2a")
    version("2.7.0", sha256="3f44d057d6f453f2ff320eb0b544b17b8ee72dbbda33823a6d600dd3859cd37e")
    version("2.6.1", sha256="a3627869e36796a7b60b07a31305e344449ea8c1fb4f76e2573fea43398454ac")
    version("2.6.0", sha256="2d9b977e5e8a0d0d96c117b5260497dba4f54032fd22f07fdc3ae80278262d01")
    version("2.5.0", sha256="d499fc9c9429cf8dee017072312e350077f27d75187e5a83dbfaad26788f5f45")
    version("2.4.0", sha256="28794a523420457e624e3054dea95d7f5834529c9f9794eb9745d4a3f0a1bc15")
    version("2.3.0", sha256="62cb62f034d688ac586b92e381620fc940ef1bd43664b064ead5d59de5aace9e")
    version("2.2.0", sha256="2d853378b186f85c952072f78f5e9533185a274fb7b2d10718527f15e12bfc7d")
    version("2.1.0", sha256="c0b1cdd95703b07209fe14cd4d2bc28fa8d1ca3d6caa3a433ad1ba3438c83f5b")
    version("2.0.0", sha256="92d5b1ac41738939902c2d16f44c42f6b4c996ab84e03c26159e70ace7048299")
    version("1.3.3", sha256="12d5b4c913063625154019b0a03a253c5b9339c969939454b81f6baaf82b34ca")
    version("1.3.2", sha256="b0223806a75a7aa4e5f404d08ee7a612f511e4fb1aad740be19ce8429c4cbe2e")
    version("1.3.0", sha256="998657c88917ece065d2f9fc2ec977dbb5c117436b989721fc9a8b147e906ff3")
    version("1.2.0", sha256="eb8fd9c3abdcd404003cf72087cabec668162a33de4fdbc34d6b2d59d24d98ad")
    version("1.1.0", sha256="7ae0da2257efa7f4ad9c224bce0d10cb1a5580df6b7010d832cf0a11def4627d")
    version("1.0.1", sha256="2adec90497141893ca53ac945b88d5881610ed3347166b36be4f72449b5342a0")
    version("1.0.0", sha256="c7a16d349e11d85891cb91ece97d5bdbc4b140f614a0265732c2dc81a806bd98")

    depends_on("cxx", type="build")  # generated
    variant("cuda", default=True, description="Build with CUDA")
    conflicts("~cuda", msg="Cutlass requires CUDA")
    conflicts(
        "cuda_arch=none",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    def setup_build_environment(self, env):
        env.set("CUDACXX", self.spec["cuda"].prefix.bin.nvcc)

    def cmake_args(self):
        cuda_arch = self.spec.variants["cuda_arch"].value
        return [self.define("CUTLASS_NVCC_ARCHS", ";".join(cuda_arch))]
