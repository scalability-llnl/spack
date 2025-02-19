# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Dyninst(CMakePackage):
    """API for dynamic binary instrumentation.  Modify programs while they
    are executing without recompiling, re-linking, or re-executing."""

    homepage = "https://dyninst.org"
    url = "https://github.com/dyninst/dyninst/archive/refs/tags/v12.2.0.tar.gz"
    git = "https://github.com/dyninst/dyninst.git"
    maintainers("hainest")

    tags = ["e4s"]

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("13.0.0", sha256="1bc48d26478b677a6c090c25586a447507bd1b4cf88d369bd61820005ce1be39")
    version("12.3.0", sha256="956b0378d2badb765a7e677c0b66c0b8b8cacca7631222bfe7a27b369abf7dd4")
    version("12.2.1", sha256="c304af3c6191e92acd27350fd9b7b02899767a0e38abb3a08a378abe01d1ef01")
    version("12.2.0", sha256="84c37efc1b220110af03f8fbb6ab295628b445c873b5115db91b64443e445a5d")
    version("12.1.0", sha256="c71c0caed12b0b65bbbd09896d0b25dde3b9062b5b2eb8426c86baa50e7af2fb")
    version("12.0.1", sha256="0d940dffd73711eb973e90d2a6ecaeb368b2b025c7db9a1cfa61716e73909041")
    version("12.0.0", sha256="829f9340cb1550efa0b69a7b4db36975ede9c70d7c0ecbad2fda91ffcec0609a")
    version("11.0.1", sha256="e80c7c786b25f931890145dd349c576f49b6031c2cad4d4c722cbcc7e9550b73")
    version("11.0.0", sha256="3b3fd2743d9312e9cb9770c8c520dd3d0730dc90584e28024664cda50f00e3b9")
    version("10.2.1", sha256="8077c6c7a12577d2ffdcd07521c1eb1b7367da94d9a7ef10bf14053aeaae7ba1")
    version("10.2.0", sha256="4212b93bef4563c7de7dce4258e899bcde52315a571087e87fde9f8040123b43")
    version("10.1.0", sha256="4a121d70c1bb020408a7a697d74602e18250c3c85800f230566fcccd593c0129")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("openmp", default=True, description="Enable OpenMP support for ParseAPI ")

    variant("static", default=False, description="Build static libraries")

    variant("stat_dysect", default=False, description="Patch for STAT's DySectAPI")

    depends_on(
        "boost+atomic+chrono+date_time+filesystem+system+thread+timer+container+random+exception"
    )
    depends_on("boost@1.61.0:", when="@10.1.0:")
    depends_on("boost@1.67.0:", when="@11.0.0:")
    depends_on("boost@1.70.0:", when="@12:12.3.0")
    depends_on("boost@1.71.0:", when="@13:")

    depends_on("libiberty+pic")

    # Parallel DWARF parsing requires a thread-safe libdw
    depends_on("elfutils", type="link")
    depends_on("elfutils@0.186:", type="link", when="@12.0.1:")
    depends_on("elfutils@0.178:", type="link", when="@10.2.0:")

    with when("@:12.3.0"):
        # findtbb.cmake in the dynist repo does not work with recent tbb
        # package layout. Need to use tbb provided config instead.
        conflicts("^intel-tbb@2021.1:")
        conflicts("^intel-oneapi-tbb@2021.1:")
        conflicts("^intel-parallel-studio")

    depends_on("tbb")
    requires("^[virtuals=tbb] intel-tbb@2019.9:", when="@13.0.0:")

    with when("@13.0.0:"):
        depends_on("cmake@3.14.0:", type="build")
        conflicts("cmake@3.19.0")

    depends_on("cmake@3.4.0:", type="build", when="@10.1.0:")

    patch("stat_dysect.patch", when="+stat_dysect")
    patch(
        "missing_include_deque.patch",
        when="@10.0.0:12.2.0",
        sha256="0064d8d51bd01bd0035e1ebc49276f627ce6366d4524c92cf47d3c09b0031f96",
    )

    requires("%gcc", when="@:13.0.0", msg="dyninst builds only with GCC")

    # No Mac support (including apple-clang)
    conflicts("platform=darwin", msg="macOS is not supported")

    # Version 11.0 requires a C++11-compliant ABI
    conflicts("%gcc@:5", when="@11.0.0:")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("Boost_ROOT_DIR", spec["boost"].prefix),
            self.define("ElfUtils_ROOT_DIR", spec["elfutils"].prefix),
            self.define("LibIberty_ROOT_DIR", spec["libiberty"].prefix),
            self.define("TBB_ROOT_DIR", spec["tbb"].prefix),
            self.define("LibIberty_LIBRARIES", spec["libiberty"].libs),
            self.define_from_variant("USE_OpenMP", "openmp"),
            self.define_from_variant("ENABLE_STATIC_LIBS", "static"),
        ]

        # Make sure Dyninst doesn't try to build its own dependencies outside of Spack
        if spec.satisfies("@10.2.0:12.3.0"):
            args.append(self.define("STERILE_BUILD", True))

        return args

    def test_ptls(self):
        """Run parseThat on /bin/ls to rewrite with basic instrumentation"""
        parseThat = which(self.prefix.bin.parseThat)
        os.environ["DYNINSTAPI_RT_LIB"] = join_path(self.prefix.lib, "libdyninstAPI_RT.so")
        parseThat(
            "--binary-edit={0:s}".format(join_path(self.test_suite.stage, "ls.rewritten")),
            "/bin/ls",
        )
