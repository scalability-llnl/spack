# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bear(CMakePackage):
    """Bear is a tool that generates a compilation database for clang tooling
    from non-cmake build systems."""

    homepage = "https://github.com/rizsotto/Bear"
    git = "git@github.com:rizsotto/Bear.git"
    url = "https://github.com/rizsotto/Bear/archive/2.0.4.tar.gz"
    maintainers("vmiheer", "trws")

    license("GPL-3.0-or-later")

    version("3.1.3", sha256="8314438428069ffeca15e2644eaa51284f884b7a1b2ddfdafe12152581b13398")
    version("3.1.2", sha256="5f94e98480bd8576a64cd1d59649f34b09b4e02a81f1d983c92af1113e061fc3")
    version("3.1.1", sha256="52f8ee68ee490e5f2714eebad9e1288e89c82b9fd7bf756f600cff03de63a119")
    version("3.1.0", sha256="33c1f4663d94508f11cbd999dd5571359be7d15b0f473f7cfbea2c0b3190a891")
    version("3.0.21", sha256="0c949a6a907bc61a1284661f8d9dab1788a62770c265f6142602669b6e5c389d")
    version("3.0.20", sha256="45cfcdab07f824f6c06c9776701156f7a04b23eadd25ecbc88c188789a447cc7")
    version("3.0.19", sha256="2fcfe2c6e029182cfc54ed26b3505c0ef12b0f43df03fb587f335afdc2ca9431")
    version("3.0.18", sha256="ae94047c79b4f48462b66981f66a67b6a833d75d4c40e7afead491b1865f1142")
    version("3.0.17", sha256="107f94e045d930e88f5f5b4b484c8df1bf4834722943525765c271e0b5b34b78")
    version("3.0.16", sha256="877ee5e89e8445f74df95f2f3896597f04b86a4e5d0dbbca07ac71027dcb362d")
    version("3.0.0", sha256="7b68aad69e887d945ad20f8e9f3a8c33cf2d59cc80da7e52d931d8c685fe2f79")
    version("2.2.0", sha256="6bd61a6d64a24a61eab17e7f2950e688820c72635e1cf7ea8ea7bf9482f3b612")
    version("2.0.4", sha256="33ea117b09068aa2cd59c0f0f7535ad82c5ee473133779f1cc20f6f99793a63e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", when="@3:")
    depends_on("fmt@8", when="@3.0.0:")
    depends_on("grpc +shared", when="@3.0.0:")
    depends_on("nlohmann-json", when="@3.0.0:")
    depends_on("spdlog", when="@3.0.0:")
    depends_on("cmake@2.8:", when="@2.0.4:", type="build")
    depends_on("cmake@3.12:", when="@3.0.0:", type="build")
    depends_on("python", type="build")
    depends_on("googletest", type="test", when="@3:")

    # specific version constraints
    conflicts("@3.0.0", when="%apple-clang@15", msg="Problems with nlohmann-json integration")
    conflicts("@3.0.0", when="%clang@13.0.1", msg="Problems with std::optional")

    # general version constraints
    conflicts("@3:", when="%gcc@:8.9", msg="Bear requires GCC with full std::filesystem support")

    patch("rpath-handling-3.0.20.patch", when="@3.0.20:")

    def cmake_args(self):
        return [
            "-DENABLE_UNIT_TESTS={}".format("ON" if self.run_tests else "OFF"),
            "-DENABLE_FUNC_TESTS=OFF",
            "-DENABLE_MULTILIB=OFF",
        ]
