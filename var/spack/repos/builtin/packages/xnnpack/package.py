# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xnnpack(CMakePackage):
    """High-efficiency floating-point neural network inference operators for
    mobile, server, and Web"""

    homepage = "https://github.com/google/XNNPACK"
    git = "https://github.com/google/XNNPACK.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2022-02-16", commit="ae108ef49aa5623b896fc93d4298c49d1750d9ba")  # py-torch@1.12
    version("2021-06-21", commit="79cd5f9e18ad0925ac9a050b00ea5a36230072db")  # py-torch@1.10:1.11
    version("2021-02-22", commit="55d53a4e7079d38e90acd75dd9e4f9e781d2da35")  # py-torch@1.8:1.9
    version("2020-03-23", commit="1b354636b5942826547055252f3b359b54acff95")  # py-torch@1.6:1.7
    version("2020-02-24", commit="7493bfb9d412e59529bcbced6a902d44cfa8ea1c")  # py-torch@1.5

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    generator("ninja")
    depends_on("cmake@3.5:", type="build")
    depends_on("python", type="build")

    resource(
        name="clog",
        url="https://github.com/pytorch/cpuinfo/archive/d5e37adf1406cf899d7d9ec1d317c47506ccb970.tar.gz",
        sha256="3f2dc1970f397a0e59db72f9fca6ff144b216895c1d606f6c94a507c1e53a025",
        destination="deps",
        placement="clog",
    )
    resource(
        name="cpuinfo",
        url="https://github.com/pytorch/cpuinfo/archive/5916273f79a21551890fd3d56fc5375a78d1598d.zip",
        sha256="2a160c527d3c58085ce260f34f9e2b161adc009b34186a2baf24e74376e89e6d",
        destination="deps",
        placement="cpuinfo",
    )
    resource(
        name="fp16",
        url="https://github.com/Maratyszcza/FP16/archive/0a92994d729ff76a58f692d3028ca1b64b145d91.zip",
        sha256="e66e65515fa09927b348d3d584c68be4215cfe664100d01c9dbc7655a5716d70",
        destination="deps",
        placement="fp16",
    )
    resource(
        name="fxdiv",
        url="https://github.com/Maratyszcza/FXdiv/archive/b408327ac2a15ec3e43352421954f5b1967701d1.zip",
        sha256="ab7dfb08829bee33dca38405d647868fb214ac685e379ec7ef2bebcd234cd44d",
        destination="deps",
        placement="fxdiv",
    )
    resource(
        name="pthreadpool",
        url="https://github.com/Maratyszcza/pthreadpool/archive/545ebe9f225aec6dca49109516fac02e973a3de2.zip",
        sha256="8461f6540ae9f777ce20d1c0d1d249e5e61c438744fb390c0c6f91940aa69ea3",
        destination="deps",
        placement="pthreadpool",
    )
    resource(
        name="psimd",
        url="https://github.com/Maratyszcza/psimd/archive/10b4ffc6ea9e2e11668f86969586f88bc82aaefa.tar.gz",
        sha256="1fefd66702cb2eb3462b962f33d4fb23d59a55d5889ee6372469d286c4512df4",
        destination="deps",
        placement="psimd",
    )

    # https://github.com/google/XNNPACK/pull/2797
    patch("2797.patch", when="@:2022-03-27")

    def cmake_args(self):
        # TODO: XNNPACK has a XNNPACK_USE_SYSTEM_LIBS option, but it seems to be broken
        # See https://github.com/google/XNNPACK/issues/1543
        return [
            self.define("CLOG_SOURCE_DIR", join_path(self.stage.source_path, "deps", "clog")),
            self.define(
                "CPUINFO_SOURCE_DIR", join_path(self.stage.source_path, "deps", "cpuinfo")
            ),
            self.define("FP16_SOURCE_DIR", join_path(self.stage.source_path, "deps", "fp16")),
            self.define("FXDIV_SOURCE_DIR", join_path(self.stage.source_path, "deps", "fxdiv")),
            self.define(
                "PTHREADPOOL_SOURCE_DIR", join_path(self.stage.source_path, "deps", "pthreadpool")
            ),
            self.define("PSIMD_SOURCE_DIR", join_path(self.stage.source_path, "deps", "psimd")),
            self.define("BUILD_SHARED_LIBS", True),
            self.define("XNNPACK_BUILD_TESTS", False),
            self.define("XNNPACK_BUILD_BENCHMARKS", False),
        ]
