# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hiredis(MakefilePackage, CMakePackage):
    """Hiredis is a minimalistic C client library for the Redis database."""

    homepage = "https://github.com/redis/hiredis"
    url = "https://github.com/redis/hiredis/archive/refs/tags/v1.0.2.tar.gz"
    git = "https://github.com/redis/hiredis.git"

    maintainers = ["lpottier"]

    version("1.0.2", sha256="e0ab696e2f07deb4252dda45b703d09854e53b9703c7d52182ce5a22616c3819")
    version("1.0.1", sha256="a420df40775ac7b4b46550dd4df78ffe6620616333496a17c9c9fc556815ba4b")
    version("1.0.0", sha256="2a0b5fe5119ec973a0c1966bfc4bd7ed39dbce1cb6d749064af9121fe971936f")
    version(
        "0.14.1",
        sha256="2663b2aed9fd430507e30fc5e63274ee40cdd1a296026e22eafd7d99b01c8913",
        deprecated=True,
    )
    version(
        "0.14.0",
        sha256="042f965e182b80693015839a9d0278ae73fae5d5d09d8bf6d0e6a39a8c4393bd",
        deprecated=True,
    )
    version(
        "0.13.3",
        sha256="717e6fc8dc2819bef522deaca516de9e51b9dfa68fe393b7db5c3b6079196f78",
        deprecated=True,
    )
    version(
        "0.13.2",
        sha256="b0cf73ebe039fe25ecaaa881acdda8bdc393ed997e049b04fc20865835953694",
        deprecated=True,
    )

    build_system(
        conditional("cmake", when="@1.0.0:"),
        conditional("makefile", when="@:0.14.1"),
        default="cmake",
    )

    variant("ssl", default=False, description="Builds with SSL enabled")
    variant("test", default=False, description="Builds test suite")
    variant("test_ssl", default=False, description="Builds  test suite for SSL")
    variant("test_async", default=False, description="Builds test suite for async primitives")

    depends_on("cmake@3.18:", type="build", when="@1.0.0:")
    depends_on("openssl@1.1:", type=("build", "link"), when="+ssl")
    depends_on("openssl@1.1:", type=("build", "link"), when="+test_ssl")

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")

    @run_after("install")
    def darwin_fix(self):
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)

    def cmake_args(self):
        build_test = not ("+test" in self.spec)
        ssl_test = ("+test_ssl" in self.spec) and ("+test" in self.spec)
        async_test = ("+test_async" in self.spec) and ("+test" in self.spec)

        args = [
            self.define_from_variant("ENABLE_SSL", "ssl"),
            self.define("DISABLE_TESTS", build_test),
            self.define("ENABLE_SSL_TESTS", ssl_test),
            self.define("ENABLE_ASYNC_TESTS", async_test),
        ]
        return args
