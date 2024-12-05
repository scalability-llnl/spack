# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RedisPlusPlus(CMakePackage):
    """Redis-plus-plus is a C++ client library for Redis and
    is based on hiredis, and is compatible with C++ 17, C++ 14,
    and C++ 11."""

    homepage = "https://github.com/sewenew/redis-plus-plus"
    url = "https://github.com/sewenew/redis-plus-plus/archive/refs/tags/1.3.6.tar.gz"

    maintainers("lpottier")

    variant("cxxstd", values=("11", "14", "17"), default="14", description="C++ standard used")
    variant("shared", default=True, description="Enables the build of a shared library")
    variant("static", default=True, description="Enables the build of a static library")
    variant(
        "fpic",
        default=True,
        description="Use Position Independent Code (-fPIC) to build the static library",
    )
    variant("test", default=False, description="Builds test suite")
    variant("tls", default=False, description="Builds with TLS support")

    license("Apache-2.0")

    version("1.3.8", sha256="ad521b4a24d1591a1564f945ba6370875b501210222e324f398065251df41641")
    version("1.3.6", sha256="87dcadca50c6f0403cde47eb1f79af7ac8dd5a19c3cad2bb54ba5a34f9173a3e")
    version("1.3.5", sha256="a49a72fef26ed39d36a278fcc4e4d92822e111697b5992d8f26f70d16edc6c1f")
    version("1.3.4", sha256="b9f2b3e0f084fe9a7360e44a9ae28aa42067fbaf027734989c778865c2d5dca5")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.18:", type="build")
    depends_on("hiredis@1.0.0:", type=("build", "link"))
    depends_on("hiredis@1.0.0:+ssl", type=("build", "link"), when="+tls")
    depends_on("openssl@1.1:", type=("build", "link"), when="+tls")

    conflicts("+tls", when="+static", msg="Static libraries cannot be built with TLS support.")

    def cmake_args(self):
        cxxstd = self.spec.variants["cxxstd"].value
        use_fpic = ("+static" in self.spec) and ("+fpic" in self.spec)

        args = [
            self.define("REDIS_PLUS_PLUS_CXX_STANDARD", cxxstd),
            self.define_from_variant("REDIS_PLUS_PLUS_USE_TLS", "tls"),
            self.define_from_variant("REDIS_PLUS_PLUS_BUILD_TEST", "test"),
            self.define_from_variant("REDIS_PLUS_PLUS_BUILD_STATIC", "static"),
            self.define_from_variant("REDIS_PLUS_PLUS_BUILD_SHARED", "shared"),
            self.define("REDIS_PLUS_PLUS_BUILD_STATIC_WITH_PIC", use_fpic),
        ]

        return args
