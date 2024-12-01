# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioNvcomp(CMakePackage, CudaPackage):
    """LibPressio Bindings for NVCOMP"""

    homepage = "https://github.com/robertu94/libpressio-nvcomp"
    url = "https://github.com/robertu94/libpressio-nvcomp/archive/refs/tags/0.0.3.tar.gz"
    git = "https://github.com/robertu94/libpressio-nvcomp"

    maintainers("robertu94")

    version("0.0.6", sha256="19ecc090b32ec77ddbdf6a3f1f823cf19c32bd8c08b0acb0f87c740961a1d9b4")
    version("0.0.5", sha256="2f2a2567c77db550badaf594cda824fa313470b143f69bcef308eeb80b4876c2")
    version("0.0.4", sha256="6ff7d0f3167dead7584c994a6a11782f20eb3dd4844307e4ee8b2aebcd8571e9")
    version("0.0.3", sha256="21409d34f9281bfd7b83b74f5f8fc6d34794f3161391405538c060fb59534597")
    version("0.0.2", commit="38d7aa7c283681cbe5b7f17b900f72f9f25be51c")

    depends_on("cxx", type="build")  # generated

    depends_on("nvcomp@2.2.0:", when="@0.0.3:")
    depends_on("libpressio+cuda")
    depends_on("libpressio@0.99.4:", when="@0.0.6:")
    depends_on("libpressio@0.89.0:", when="@0.0.3:0.0.5")
    depends_on("libpressio@0.88.0:", when="@:0.0.2")

    conflicts("~cuda")
    conflicts("cuda_arch=none", when="+cuda")

    def cmake_args(self):
        cuda_arch = self.spec.variants["cuda_arch"].value
        args = [("-DCMAKE_CUDA_ARCHITECTURES=%s" % cuda_arch)]
        return args
