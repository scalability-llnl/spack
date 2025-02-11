# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Quantlib(CMakePackage):
    """The QuantLib project is aimed at providing a comprehensive software
    framework for quantitative finance. QuantLib is a free/open-source library
    for modeling, trading, and risk management in real-life."""

    homepage = "https://www.quantlib.org/"
    url = "https://github.com/lballabio/QuantLib/releases/download/v1.31.1/QuantLib-1.31.1.tar.gz"

    maintainers("TheQueasle")

    version("1.34", sha256="eb87aa8ced76550361771e167eba26aace018074ec370f7af49a01aa56b2fe50")
    version("1.31.1", sha256="13b5346217153ae3c185e0c640cc523a1a6522c3a721698b2c255fd9a1a15a68")

    variant("benchmark", default=True, description="Build benchmark")
    variant("examples", default=True, description="Build examples")
    variant("test", default=True, description="Build test suite")
    variant("openmp", default=False, description="Detect and use OpenMP")
    variant("punit", default=False, description="Enable the parallel unit test runner")
    variant(
        "sessions",
        default=False,
        description="Singletons return different instances for different sessions",
    )
    variant("threadsafe", default=False, description="Enable the thread-safe observer pattern")
    variant("tracing", default=False, description="Tracing messages should be allowed")
    variant(
        "errorfunctions",
        default=False,
        description="Error messages should include current function information",
    )
    variant(
        "errorlines",
        default=False,
        description="Error messages should include file and line information",
    )
    variant("extra", default=False, description="Extra safety checks should be performed")
    variant("highres", default=False, description="Enable date resolution down to microseconds")
    variant(
        "null",
        default=False,
        description="Enable the implementation of Null as template functions",
    )
    variant("tagged", default=False, description="Library names use layout tags")
    variant("tidy", default=False, description="Use clang-tidy when building")
    variant("indexed", default=False, description="Use indexed coupons instead of par coupons")
    variant("std", default=True, description="Enable all QL_USE_STD_* options")

    depends_on("boost")

    def cmake_args(self):
        args = []

        args = [
            self.define_from_variant("QL_BUILD_BENCHMARK", "benchmark"),
            self.define_from_variant("QL_INSTALL_BENCHMARK", "benchmark"),
        ]

        if "+examples" in self.spec:
            args += ["-DQL_BUILD_EXAMPLES=ON", "-DQL_INSTALL_EXAMPLES=ON"]
        else:
            args += ["-DQL_BUILD_EXAMPLES=OFF", "-DQL_INSTALL_EXAMPLES=OFF"]

        if "+test" in self.spec:
            args += ["-DQL_BUILD_TEST_SUITE=ON", "-DQL_INSTALL_TEST_SUITE=ON"]
        else:
            args += ["-DQL_BUILD_TEST_SUITE=OFF", "-DQL_INSTALL_TEST_SUITE=OFF"]

        if "+openmp" in self.spec:
            args += ["-DQL_ENABLE_OPENMP=ON"]
        else:
            args += ["-DQL_ENABLE_OPENMP=OFF"]

        if "+punit" in self.spec:
            args += ["-DQL_ENABLE_PARALLEL_UNIT_TEST_RUNNER=ON"]
        else:
            args += ["-DQL_ENABLE_PARALLEL_UNIT_TEST_RUNNER=OFF"]

        if "+sessions" in self.spec:
            args += ["-DQL_ENABLE_SESSIONS=ON"]
        else:
            args += ["-DQL_ENABLE_SESSIONS=OFF"]

        if "+threadsafe" in self.spec:
            args += ["-DQL_ENABLE_THREAD_SAFE_OBSERVER_PATTERN=ON"]
        else:
            args += ["-DQL_ENABLE_THREAD_SAFE_OBSERVER_PATTERN=OFF"]

        if "+tracing" in self.spec:
            args += ["-DQL_ENABLE_TRACING=ON"]
        else:
            args += ["-DQL_ENABLE_TRACING=OFF"]

        if "+errorfunctions" in self.spec:
            args += ["-DQL_ERROR_FUNCTIONS=ON"]
        else:
            args += ["-DQL_ERROR_FUNCTIONS=OFF"]

        if "+errorlines" in self.spec:
            args += ["-DQL_ERROR_LINES=ON"]
        else:
            args += ["-DQL_ERROR_LINES=OFF"]

        if "+extra" in self.spec:
            args += ["-DQL_EXTRA_SAFETY_CHECKS=ON"]
        else:
            args += ["-DQL_EXTRA_SAFETY_CHECKS=OFF"]

        if "+high" in self.spec:
            args += ["-DQL_HIGH_RESOLUTION_DATE=ON"]
        else:
            args += ["-DQL_HIGH_RESOLUTION_DATE=OFF"]

        if "+null" in self.spec:
            args += ["-DQL_NULL_AS_FUNCTIONS=ON"]
        else:
            args += ["-DQL_NULL_AS_FUNCTIONS=OFF"]

        if "+tagged" in self.spec:
            args += ["-DQL_TAGGED_LAYOUT=ON"]
        else:
            args += ["-DQL_TAGGED_LAYOUT=OFF"]

        if "+tidy" in self.spec:
            args += ["-DQL_USE_CLANG_TIDY=ON"]
        else:
            args += ["-DQL_USE_CLANG_TIDY=OFF"]

        if "+indexed" in self.spec:
            args += ["-DQL_USE_INDEXED_COUPON=ON"]
        else:
            args += ["-DQL_USE_INDEXED_COUPON=OFF"]

        if "+std" in self.spec:
            args += ["-DQL_USE_STD_CLASSES=ON"]
        else:
            args += ["-DQL_USE_STD_CLASSES=OFF"]

        return args

    # The Quantlib build process creates the `quantlib-config` file but it is
    # not part of the paths that get installed via spack.  This function updates
    # that file to include the spack paths needed and then copies the file from the
    # build directory to the prefix.bin directory.
    @run_after("cmake")
    def install_quantlib_config(self):
        import os

        prefix = self.spec.prefix
        mkdirp(prefix.bin)
        filter_file(r"^prefix=.*", f"prefix={prefix}", join_path(self.build_directory, "quantlib-config"))
        install(join_path(self.build_directory, "quantlib-config"), prefix.bin)
