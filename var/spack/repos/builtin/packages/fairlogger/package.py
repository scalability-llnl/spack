# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
#   Spack Project Developers. See the top-level COPYRIGHT file for details.
# Copyright 2020 GSI Helmholtz Centre for Heavy Ion Research GmbH,
#   Darmstadt, Germany
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fairlogger(CMakePackage):
    """Lightweight and fast C++ Logging Library"""

    homepage = "https://github.com/FairRootGroup/FairLogger"
    url = "https://github.com/FairRootGroup/FairLogger/archive/v1.2.0.tar.gz"
    git = "https://github.com/FairRootGroup/FairLogger.git"
    maintainers("dennisklein", "ChristianTackeGSI")

    version("develop", branch="dev", get_full_repo=True)
    version("1.11.1", sha256="bba5814f101d705792499e43b387190d8b8c7592466171ae045d4926485f2f70")
    version("1.10.4", sha256="2fa321893f2c8c599cca160db243299ce1e941fbfb3f935b1139caa943bc0dba")
    version("1.9.3", sha256="0c02076ed708372d5ae7bdebcefc8e45a8cbfa480eea781308336d60a2781f3a")
    version(
        "1.9.0",
        sha256="13bcaa0d4129f8d4e69a0a2ece8e5b7073760082c8aa028e3fc0c11106503095",
        deprecated=True,
    )
    version(
        "1.8.0",
        sha256="3f0a38dba1411b542d998e02badcc099c057b33a402954fc5c2ab74947a0c42c",
        deprecated=True,
    )
    version(
        "1.7.0",
        sha256="ef467f0a70afc0549442323d70b165fa0b0b4b4e6f17834573ca15e8e0b007e4",
        deprecated=True,
    )
    version(
        "1.6.2",
        sha256="5c6ef0c0029eb451fee71756cb96e6c5011040a9813e8889667b6f3b6b04ed03",
        deprecated=True,
    )
    version(
        "1.6.1",
        sha256="3894580f4c398d724ba408e410e50f70c9f452e8cfaf7c3ff8118c08df28eaa8",
        deprecated=True,
    )
    version(
        "1.6.0",
        sha256="721e8cadfceb2f63014c2a727e098babc6deba653baab8866445a772385d0f5b",
        deprecated=True,
    )
    version(
        "1.5.0",
        sha256="8e74e0b1e50ee86f4fca87a44c6b393740b32099ac3880046bf252c31c58dd42",
        deprecated=True,
    )
    version(
        "1.4.0",
        sha256="75457e86984cc03ce87d6ad37adc5aab1910cabd39a9bbe5fb21ce2475a91138",
        deprecated=True,
    )
    version(
        "1.3.0",
        sha256="5cedea2773f7091d69aae9fd8f724e6e47929ee3784acdd295945a848eb36b93",
        deprecated=True,
    )
    version(
        "1.2.0",
        sha256="bc0e049cf84ceb308132d8679e7f22fcdca5561dda314d5233d0d5fe2b0f8c62",
        deprecated=True,
    )
    version(
        "1.1.0",
        sha256="e185e5bd07df648224f85e765d18579fae0de54adaab9a194335e3ad6d3d29f7",
        deprecated=True,
    )
    version(
        "1.0.6",
        sha256="2fc266a6e494adda40837be406aef8d9838f385ffd64fbfafb1164833906b4e0",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    generator("make", "ninja", default="ninja")

    variant(
        "build_type",
        default="RelWithDebInfo",
        values=("Debug", "Release", "RelWithDebInfo"),
        multi=False,
        description="CMake build type",
    )
    variant(
        "cxxstd",
        default="default",
        values=("default", conditional("11", when="@:1.9"), "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    variant(
        "pretty", default=False, description="Use BOOST_PRETTY_FUNCTION macro (Supported by 1.4+)."
    )
    conflicts("+pretty", when="@:1.3")

    depends_on("cmake@3.9.4:", type="build")
    depends_on("git", type="build", when="@develop")

    depends_on("boost", when="+pretty")
    conflicts("^boost@1.70:", when="^cmake@:3.14")
    depends_on("fmt@:8", when="@:1.9")
    depends_on("fmt@5.3.0:5", when="@1.6.0:1.6.1")
    depends_on("fmt@5.3.0:", when="@1.6.2:")

    def patch(self):
        """FairLogger gets its version number from git.
        But the tarball doesn't have that information, so
        we patch the spack version into CMakeLists.txt"""
        if not self.spec.satisfies("@develop"):
            filter_file(
                r"(get_git_version\(.*)\)",
                rf"\1 DEFAULT_VERSION {self.spec.version})",
                "CMakeLists.txt",
            )

    def cmake_args(self):
        args = [self.define("DISABLE_COLOR", True)]
        if self.spec.variants["cxxstd"].value != "default":
            args.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        if self.spec.satisfies("@1.4:"):
            args.append(self.define_from_variant("USE_BOOST_PRETTY_FUNCTION", "pretty"))
        if self.spec.satisfies("@1.6:"):
            args.append(self.define("USE_EXTERNAL_FMT", True))
        if self.spec.satisfies("^boost@:1.69"):
            args.append(self.define("Boost_NO_BOOST_CMAKE", True))
        return args
