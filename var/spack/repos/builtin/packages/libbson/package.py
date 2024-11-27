# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import cmake
from spack.package import *


class Libbson(AutotoolsPackage, CMakePackage):
    """libbson is a library providing useful routines related to building,
    parsing, and iterating BSON documents."""

    homepage = "https://github.com/mongodb/mongo-c-driver"
    url = "https://github.com/mongodb/mongo-c-driver/archive/refs/tags/1.25.0.tar.gz"

    maintainers("michaelkuhn")

    version("1.27.2", sha256="a53010803e2df097a2ea756be6ece34c8f52cda2c18e6ea21115097b75f5d4bf")
    version("1.24.4", sha256="2f4a3e8943bfe3b8672c2053f88cf74acc8494dc98a45445f727901eee141544")
    version("1.23.4", sha256="209406c91fcf7c63aa633179a0a6b1b36ba237fb77e0470fd81f7299a408e334")
    version("1.23.3", sha256="c8f951d4f965d455f37ae2e10b72914736fc0f25c4ffc14afc3cbadd1a574ef6")
    version("1.23.2", sha256="123c358827eea07cd76a31c40281bb1c81b6744f6587c96d0cf217be8b1234e3")
    version("1.21.0", sha256="840ff79480070f98870743fbb332e2c10dd021b6b9c952d08010efdda4d70ee4")
    version("1.17.6", sha256="8644deec7ae585e8d12566978f2017181e883f303a028b5b3ccb83c91248b150")
    version("1.17.5", sha256="4b15b7e73a8b0621493e4368dc2de8a74af381823ae8f391da3d75d227ba16be")
    version("1.17.0", sha256="90aa23a3f92be0a076fe0b903b68276a7973d4e472929943069f503d5ab50cb9")
    version("1.16.2", sha256="0a722180e5b5c86c415b9256d753b2d5552901dc5d95c9f022072c3cd336887e")
    version("1.9.5", sha256="6bb51b863a4641d6d7729e4b55df8f4389ed534c34eb3a1cda906a53df11072c")
    version("1.9.4", sha256="c3cc230a3451bf7fedc5bb34c3191fd23d841e65ec415301f6c77e531924b769")
    version("1.9.3", sha256="244e786c746fe6326433b1a6fcaadbdedc0da3d11c7b3168f0afa468f310e5f1")
    version("1.9.1", sha256="236d9fcec0fe419c2201481081e497f49136eda2349b61cfede6233013bf7601")
    version("1.8.1", sha256="9d18d14671b7890e27b2a5ce33a73a5ed5d33d39bba70209bae99c1dc7aa1ed4")
    version("1.8.0", sha256="63dea744b265a2e17c7b5e289f7803c679721d98e2975ea7d56bc1e7b8586bc1")
    version("1.7.0", sha256="442d89e89dfb43bba1f65080dc61fdcba01dcb23468b2842c1dbdd4acd6049d3")
    version("1.6.3", sha256="e9e4012a9080bdc927b5060b126a2c82ca11e71ebe7f2152d079fa2ce461a7fb")
    version("1.6.2", sha256="aad410123e4bd8a9804c3c3d79e03344e2df104872594dc2cf19605d492944ba")
    version(
        "1.6.1",
        sha256="5f160d44ea42ce9352a7a3607bc10d3b4b22d3271763aa3b3a12665e73e3a02d",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    with when("build_system=cmake"):
        depends_on("cmake@3.1:", type="build")

    with when("build_system=autotools"):
        depends_on("autoconf", type="build", when="@1.6.1")
        depends_on("automake", type="build", when="@1.6.1")
        depends_on("libtool", type="build", when="@1.6.1")

    build_system(
        conditional("cmake", when="@1.10:"),
        conditional("autotools", when="@:1.9"),
        default="cmake",
    )

    def url_for_version(self, version):
        if version >= Version("1.25.0"):
            return f"https://github.com/mongodb/mongo-c-driver/archive/refs/tags/{version}.tar.gz"
        if version >= Version("1.10.0"):
            return f"https://github.com/mongodb/mongo-c-driver/releases/download/{version}/mongo-c-driver-{version}.tar.gz"
        else:
            return f"https://github.com/mongodb/libbson/releases/download/{version}/libbson-{version}.tar.gz"

    @property
    def force_autoreconf(self):
        # 1.6.1 tarball is broken
        return self.spec.satisfies("@1.6.1")


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return [
            self.define("ENABLE_AUTOMATIC_INIT_AND_CLEANUP", False),
            self.define("ENABLE_MONGOC", False),
            self.define("MONGO_USE_CCACHE", False),
            self.define("MONGO_USE_LLD", False),
        ]
