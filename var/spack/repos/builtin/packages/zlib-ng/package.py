# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class ZlibNg(AutotoolsPackage, CMakePackage):
    """zlib replacement with optimizations for next generation systems."""

    homepage = "https://github.com/zlib-ng/zlib-ng"
    url = "https://github.com/zlib-ng/zlib-ng/archive/2.0.0.tar.gz"
    git = "https://github.com/zlib-ng/zlib-ng.git"

    maintainers("haampie")

    license("Zlib")

    version("2.1.6", sha256="a5d504c0d52e2e2721e7e7d86988dec2e290d723ced2307145dedd06aeb6fef2")
    version("2.1.5", sha256="3f6576971397b379d4205ae5451ff5a68edf6c103b2f03c4188ed7075fbb5f04")
    version("2.1.4", sha256="a0293475e6a44a3f6c045229fe50f69dc0eebc62a42405a51f19d46a5541e77a")
    version(
        "2.1.3",
        sha256="d20e55f89d71991c59f1c5ad1ef944815e5850526c0d9cd8e504eaed5b24491a",
        deprecated=True,
    )
    version(
        "2.1.2",
        sha256="383560d6b00697c04e8878e26c0187b480971a8bce90ffd26a5a7b0f7ecf1a33",
        deprecated=True,
    )
    version("2.0.7", sha256="6c0853bb27738b811f2b4d4af095323c3d5ce36ceed6b50e5f773204fb8f7200")
    version("2.0.0", sha256="86993903527d9b12fc543335c19c1d33a93797b3d4d37648b5addae83679ecd8")

    variant("compat", default=True, description="Enable compatibility API")
    variant("opt", default=True, description="Enable optimizations")

    provides("zlib-api", when="+compat")

    # Default to autotools, since cmake would result in circular dependencies if it's not
    # reused.
    build_system("autotools", "cmake", default="autotools")

    # rpath shenanigans, see https://github.com/zlib-ng/zlib-ng/pull/1546
    with when("@2.1.3"):
        patch("pr-1546.patch", when="platform=darwin")
        patch("pr-1542.patch")  # fix sse4.2 detection
        patch("pr-1561.patch", when="build_system=autotools")  # drop bash dependency
        patch("pr-1562.patch")  # improve intrinsics detection

    with when("build_system=cmake"):
        depends_on("cmake@3.5.1:", type="build")
        depends_on("cmake@3.14.0:", type="build", when="@2.1.0:")

    @property
    def libs(self):
        name = "libz" if self.spec.satisfies("+compat") else "libz-ng"
        return find_libraries(name, root=self.prefix, recursive=True, shared=True)


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []
        if self.spec.satisfies("+compat"):
            args.append("--zlib-compat")
        if self.spec.satisfies("~opt"):
            args.append("--without-optimizations")
        return args

    @run_after("configure")
    def patch_makefiles(self):
        # We need to fix the building with compilers that are not recognized as gcc. Note that a
        # compiler is recognized as gcc if it has "gcc" or "clang" substring either in its
        # executable name (including the path) or in the output generated with the `-v` flag (i.e
        # '$CC -v 2>&1'). The latter is the reason why, for example, %intel and %oneapi are often
        # recognized as gcc: they almost always contain "gcc" in the verbose output. Although we
        # should not rely on the false positive results of the configure script but patch the
        # makefile for all the aforementioned compilers, we try to be conservative for now and do
        # the patching only for compilers that will fail to build the package otherwise.
        if self.spec.compiler.name not in ["nvhpc"]:
            return

        root_makefile = join_path(self.build_directory, "Makefile")
        arch_makefile = find(join_path(self.build_directory, "arch"), "Makefile", recursive=True)
        all_makefiles = arch_makefile + [root_makefile]

        with keep_modification_time(*all_makefiles):
            if self.spec.satisfies("+opt"):
                # The configure script checks whether the compiler supports the '-fno-lto' flag
                # only if it is recognized as gcc. Otherwise, it assumes that the flag is
                # supported, which is not always true:
                filter_file(r"^(NOLTOFLAG *=).*$", r"\1", *arch_makefile)

            # The configure script sets the PIC flag only if the compiler is recognized as gcc:
            filter_file(
                r"^(SFLAGS *=.*)$", r"\1 {0}".format(self.pkg.compiler.cc_pic_flag), *all_makefiles
            )

            # The configure script sets the library versioning flags only if the compiler is
            # recognized as gcc:
            if self.spec.platform in ["linux", "cray"]:
                filter_file(
                    r"^(LDSHAREDFLAGS *=.*)$",
                    r"\1 -Wl,"
                    r"-soname,$(LIBNAME1).so.$(VER1),--version-script,$(SRCDIR)/$(LIBNAME2).map",
                    root_makefile,
                )


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return [
            self.define_from_variant("ZLIB_COMPAT", "compat"),
            self.define_from_variant("WITH_OPTIM", "opt"),
        ]
