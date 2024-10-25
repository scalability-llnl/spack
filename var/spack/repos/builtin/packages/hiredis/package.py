# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hiredis(MakefilePackage, CMakePackage):
    """Hiredis is a minimalistic C client library for the Redis database."""

    homepage = "https://github.com/redis/hiredis"
    url = "https://github.com/redis/hiredis/archive/refs/tags/v1.1.0.tar.gz"
    git = "https://github.com/redis/hiredis.git"

    maintainers("lpottier", "rblake-llnl")

    license("BSD-3-Clause")

    version("1.1.0", sha256="fe6d21741ec7f3fc9df409d921f47dfc73a4d8ff64f4ac6f1d95f951bf7f53d6")
    version("1.0.2", sha256="e0ab696e2f07deb4252dda45b703d09854e53b9703c7d52182ce5a22616c3819")
    version("1.0.1", sha256="a420df40775ac7b4b46550dd4df78ffe6620616333496a17c9c9fc556815ba4b")
    version("1.0.0", sha256="2a0b5fe5119ec973a0c1966bfc4bd7ed39dbce1cb6d749064af9121fe971936f")
    version("0.14.1", sha256="2663b2aed9fd430507e30fc5e63274ee40cdd1a296026e22eafd7d99b01c8913")
    version("0.14.0", sha256="042f965e182b80693015839a9d0278ae73fae5d5d09d8bf6d0e6a39a8c4393bd")
    version("0.13.3", sha256="717e6fc8dc2819bef522deaca516de9e51b9dfa68fe393b7db5c3b6079196f78")
    version("0.13.2", sha256="b0cf73ebe039fe25ecaaa881acdda8bdc393ed997e049b04fc20865835953694")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_system(
        conditional("cmake", when="@1:"), conditional("makefile", when="@:0"), default="cmake"
    )

    variant("ssl", default=False, description="Builds with SSL enabled")
    variant("test", default=False, description="Builds test suite")
    variant("test_ssl", default=False, description="Builds  test suite for SSL")
    variant("test_async", default=False, description="Builds test suite for async primitives")

    depends_on("cmake@3.18:", type="build", when="build_system=cmake")
    depends_on("openssl@1.1:", type=("build", "link"), when="+ssl")
    depends_on("openssl@1.1:", type=("build", "link"), when="+test_ssl")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    @property
    def build_targets(self):
        use_ssl = 1 if self.spec.satisfies("+ssl") else 0
        run_test_async = 1 if self.spec.satisfies("+test_async") else 0
        return ["USE_SSL={0}".format(use_ssl), "TEST_ASYNC={0}".format(run_test_async)]

    def install(self, pkg, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")
        if (
            self.spec.satisfies("+test")
            or self.spec.satisfies("+test_async")
            or self.spec.satisfies("+test_ssl")
        ):
            make("PREFIX={0}".format(prefix), "test")

    @run_after("install")
    def darwin_fix(self):
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        build_test = not self.spec.satisfies("+test")
        ssl_test = self.spec.satisfies("+test_ssl") and self.spec.satisfies("+test")
        async_test = self.spec.satisfies("+test_async") and self.spec.satisfies("+test")

        args = [
            self.define_from_variant("ENABLE_SSL", "ssl"),
            self.define("DISABLE_TESTS", build_test),
            self.define("ENABLE_SSL_TESTS", ssl_test),
            self.define("ENABLE_ASYNC_TESTS", async_test),
        ]
        return args
