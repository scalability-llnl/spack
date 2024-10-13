# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

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
    version("10.0.0", sha256="542fccf5c57c4fe784b1a9a9e3db01d40b16ad04e7174dc6f7eb23440485ba06")
    version(
        "9.3.2", tag="v9.3.2", commit="5d2ddacb273682daa014ae22f17f3575e05b411e", deprecated=True
    )
    version(
        "9.3.0", tag="v9.3.0", commit="9b8e9c1f16d4616b827d2d36955604a8e3fb915c", deprecated=True
    )
    version(
        "9.2.0", tag="v9.2.0", commit="3a6ad66df7294417cf61618acdcfcc0fecccb045", deprecated=True
    )
    version(
        "9.1.0", tag="v9.1.0", commit="df6d090061bae7ff2ba5a6bd57bb2ecbf538ef7a", deprecated=True
    )
    version(
        "8.2.1", tag="v8.2.1", commit="939afcbad1a8273636a3686a31b51dae4f1f0c11", deprecated=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "openmp",
        default=True,
        description="Enable OpenMP support for ParseAPI " "(version 10.0.0 or later)",
    )

    variant("static", default=False, description="Build static libraries")

    variant("stat_dysect", default=False, description="Patch for STAT's DySectAPI")

    boost_libs = "+atomic+chrono+date_time+filesystem+system+thread+timer"
    "+container+random+exception"

    depends_on("boost@1.61.0:" + boost_libs, when="@10.1.0:")
    depends_on("boost@1.61.0:1.69" + boost_libs, when="@:10.0")
    depends_on("boost@1.67.0:" + boost_libs, when="@11.0.0:")
    depends_on("boost@1.70.0:" + boost_libs, when="@12:12.3.0")
    depends_on("boost@1.71.0:" + boost_libs, when="@13:")

    depends_on("libiberty+pic")

    # Dyninst uses elfutils starting with 9.3.0, and used libelf
    # before that.
    # NB: Parallel DWARF parsing in Dyninst 10.2.0 requires a thread-
    #     safe libdw
    depends_on("elfutils@0.186:", type="link", when="@12.0.1:")
    depends_on("elfutils@0.178:", type="link", when="@10.2.0:")
    depends_on("elfutils", type="link", when="@9.3.0:10.1")
    depends_on("libelf", type="link", when="@:9.2")

    # Dyninst uses libdw from elfutils starting with 10.0, and used
    # libdwarf before that.
    depends_on("libdwarf", when="@:9")

    with when("@:12.3.0"):
        # findtbb.cmake in the dynist repo does not work with recent tbb
        # package layout. Need to use tbb provided config instead.
        conflicts("^intel-tbb@2021.1:")
        conflicts("^intel-oneapi-tbb@2021.1:")
        conflicts("^intel-parallel-studio")

    depends_on("intel-tbb@2019.9:", when="@13.0.0:")
    depends_on("tbb@2018.6.0:", when="@10.0.0:12.3.0")

    with when("@13.0.0:"):
        depends_on("cmake@3.14.0:", type="build")
        conflicts("cmake@3.19.0")

    depends_on("cmake@3.4.0:", type="build", when="@10.1.0:")
    depends_on("cmake@3.0.0:", type="build", when="@10.0.0:10.0")
    depends_on("cmake@2.8:", type="build", when="@:9")

    patch("stat_dysect.patch", when="+stat_dysect")
    patch("stackanalysis_h.patch", when="@9.2.0")
    patch("v9.3.2-auto.patch", when="@9.3.2 %gcc@:4.7")
    patch("tribool.patch", when="@9.3.0:10.0.0 ^boost@1.69:")

    requires("%gcc", when="@:13.0.0", msg="dyninst builds only with GCC")

    # No Mac support (including apple-clang)
    conflicts("platform=darwin", msg="macOS is not supported")

    # Version 11.0 requires a C++11-compliant ABI
    conflicts("%gcc@:5", when="@11.0.0:")

    # Versions 9.3.x used cotire, but have no knob to turn it off.
    # Cotire has no real use for one-time builds and can break
    # parallel builds with both static and shared libs.
    @when("@9.3.0:9.3")
    def patch(self):
        filter_file("USE_COTIRE true", "USE_COTIRE false", "cmake/shared.cmake")

    # New style cmake args, starting with 10.1.
    @when("@10.1.0:")
    def cmake_args(self):
        spec = self.spec

        args = [
            "-DBoost_ROOT_DIR=%s" % spec["boost"].prefix,
            "-DElfUtils_ROOT_DIR=%s" % spec["elf"].prefix,
            "-DLibIberty_ROOT_DIR=%s" % spec["libiberty"].prefix,
            "-DTBB_ROOT_DIR=%s" % spec["tbb"].prefix,
            self.define("LibIberty_LIBRARIES", spec["libiberty"].libs),
        ]

        if spec.satisfies("+openmp"):
            args.append("-DUSE_OpenMP=ON")
        else:
            args.append("-DUSE_OpenMP=OFF")

        if spec.satisfies("+static"):
            args.append("-DENABLE_STATIC_LIBS=YES")
        else:
            args.append("-DENABLE_STATIC_LIBS=NO")

        # Make sure Dyninst doesn't try to build its own dependencies
        # outside of Spack
        if spec.satisfies("@10.2.0:12.3.0"):
            args.append("-DSTERILE_BUILD=ON")

        return args

    # Old style cmake args, up through 10.0.
    @when("@:10.0")
    def cmake_args(self):
        spec = self.spec

        # Elf -- the directory containing libelf.h.
        elf = spec["elf"].prefix
        elf_include = os.path.dirname(find_headers("libelf", elf.include, recursive=True)[0])

        # Dwarf -- the directory containing elfutils/libdw.h or
        # libdwarf.h, and the path to libdw.so or libdwarf.so.
        if spec.satisfies("@10.0.0:"):
            dwarf_include = elf.include
            dwarf_lib = find_libraries("libdw", elf, recursive=True)
        else:
            dwarf_include = spec["libdwarf"].prefix.include
            dwarf_lib = spec["libdwarf"].libs

        args = [
            "-DPATH_BOOST=%s" % spec["boost"].prefix,
            "-DIBERTY_LIBRARIES=%s" % spec["libiberty"].libs,
            "-DLIBELF_INCLUDE_DIR=%s" % elf_include,
            "-DLIBELF_LIBRARIES=%s" % spec["elf"].libs,
            "-DLIBDWARF_INCLUDE_DIR=%s" % dwarf_include,
            "-DLIBDWARF_LIBRARIES=%s" % dwarf_lib,
        ]

        # TBB include and lib directories, version 10.x or later.
        if spec.satisfies("@10.0.0:"):
            args.extend(
                [
                    "-DTBB_INCLUDE_DIRS=%s" % spec["tbb"].prefix.include,
                    "-DTBB_LIBRARY=%s" % spec["tbb"].prefix.lib,
                ]
            )

        # Openmp applies to version 10.x or later.
        if spec.satisfies("@10.0.0:"):
            if spec.satisfies("+openmp"):
                args.append("-DUSE_OpenMP=ON")
            else:
                args.append("-DUSE_OpenMP=OFF")

        # Static libs started with version 9.1.0.
        if spec.satisfies("@9.1.0:"):
            if spec.satisfies("+static"):
                args.append("-DENABLE_STATIC_LIBS=1")
            else:
                args.append("-DENABLE_STATIC_LIBS=NO")

        return args

    def test_ptls(self):
        """Run parseThat on /bin/ls to rewrite with basic instrumentation"""
        parseThat = which(self.prefix.bin.parseThat)
        os.environ["DYNINSTAPI_RT_LIB"] = join_path(self.prefix.lib, "libdyninstAPI_RT.so")
        parseThat(
            "--binary-edit={0:s}".format(join_path(self.test_suite.stage, "ls.rewritten")),
            "/bin/ls",
        )
