# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Assimp(CMakePackage):
    """Open Asset Import Library (Assimp) is a portable Open Source library to
    import various well-known 3D model formats in a uniform manner."""

    homepage = "https://www.assimp.org"
    url = "https://github.com/assimp/assimp/archive/v4.0.1.tar.gz"
    git = "https://github.com/assimp/assimp.git"

    maintainers("wdconinc")

    license("BSD-3-Clause", checked_by="wdconinc")

    version("master", branch="master")
    version("5.4.3", sha256="66dfbaee288f2bc43172440a55d0235dfc7bf885dda6435c038e8000e79582cb")
    version("5.4.2", sha256="7414861a7b038e407b510e8b8c9e58d5bf8ca76c9dfe07a01d20af388ec5086a")
    version("5.4.0", sha256="a90f77b0269addb2f381b00c09ad47710f2aab6b1d904f5e9a29953c30104d3f")
    version("5.3.1", sha256="a07666be71afe1ad4bc008c2336b7c688aca391271188eb9108d0c6db1be53f1")
    version("5.2.5", sha256="b5219e63ae31d895d60d98001ee5bb809fb2c7b2de1e7f78ceeb600063641e1a")
    version("5.2.4", sha256="6a4ff75dc727821f75ef529cea1c4fc0a7b5fc2e0a0b2ff2f6b7993fe6cb54ba")
    version("5.2.3", sha256="b20fc41af171f6d8f1f45d4621f18e6934ab7264e71c37cd72fd9832509af2a8")
    version("5.2.2", sha256="ad76c5d86c380af65a9d9f64e8fc57af692ffd80a90f613dfc6bd945d0b80bb4")
    version("5.2.1", sha256="c9cbbc8589639cd8c13f65e94a90422a70454e8fa150cf899b6038ba86e9ecff")
    version("5.1.4", sha256="bd32cdc27e1f8b7ac09d914ab92dd81d799c97e9e47315c1f40dcb7c6f7938c6")
    version("5.1.3", sha256="50a7bd2c8009945e1833c591d16f4f7c491a3c6190f69d9d007167aadb175c35")
    version("5.0.1", sha256="11310ec1f2ad2cd46b95ba88faca8f7aaa1efe9aa12605c55e3de2b977b3dbfc")
    version("4.0.1", sha256="60080d8ab4daaab309f65b3cffd99f19eb1af8d05623fff469b9b652818e286e")

    patch(
        "https://patch-diff.githubusercontent.com/raw/assimp/assimp/pull/4203.patch?full_index=1",
        sha256="24135e88bcef205e118f7a3f99948851c78d3f3e16684104dc603439dd790d74",
        when="@5.1:5.2.2",
    )

    variant("shared", default=True, description="Enables the build of shared libraries")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.10:", type="build", when="@5.1:")
    depends_on("cmake@3.22:", type="build", when="@5.4:")

    depends_on("pkgconfig", type="build")
    depends_on("zlib-api")

    def patch(self):
        filter_file("-Werror", "", "code/CMakeLists.txt")

    def cmake_args(self):
        args = [
            self.define("ASSIMP_HUNTER_ENABLED", False),
            self.define("ASSIMP_BUILD_ZLIB", False),
            self.define("ASSIMP_BUILD_MINIZIP", False),
            self.define("ASSIMP_BUILD_TESTS", self.run_tests),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == "cxxflags":
            flags.append(self.compiler.cxx11_flag)
        return (None, None, flags)

    def check(self):
        unit = Executable(join_path(self.builder.build_directory, "bin", "unit"))
        skipped_tests = [
            "AssimpAPITest_aiMatrix3x3.aiMatrix3FromToTest",
            "AssimpAPITest_aiMatrix4x4.aiMatrix4FromToTest",
            "AssimpAPITest_aiQuaternion.aiQuaternionFromNormalizedQuaternionTest",
        ]
        unit(f"--gtest_filter=-{':'.join(skipped_tests)}")
