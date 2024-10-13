# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.build_systems.cmake
import spack.build_systems.generic
from spack.package import *


class Superlu(CMakePackage, Package):
    """SuperLU is a general purpose library for the direct solution of large,
    sparse, nonsymmetric systems of linear equations on high performance
    machines. SuperLU is designed for sequential machines."""

    homepage = "https://portal.nersc.gov/project/sparse/superlu/"
    url = "https://github.com/xiaoyeli/superlu/archive/refs/tags/v5.3.0.tar.gz"

    tags = ["e4s"]

    test_requires_compiler = True

    license("BSD-3-Clause")

    version("6.0.0", sha256="5c199eac2dc57092c337cfea7e422053e8f8229f24e029825b0950edd1d17e8e")
    version(
        "5.3.0",
        sha256="3e464afa77335de200aeb739074a11e96d9bef6d0b519950cfa6684c4be1f350",
        preferred=True,
    )
    version("5.2.2", sha256="470334a72ba637578e34057f46948495e601a5988a602604f5576367e606a28c")
    version("5.2.1", sha256="28fb66d6107ee66248d5cf508c79de03d0621852a0ddeba7301801d3d859f463")
    version(
        "4.3",
        sha256="169920322eb9b9c6a334674231479d04df72440257c17870aaa0139d74416781",
        url="https://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_4.3.tar.gz",
    )
    version(
        "4.2",
        sha256="5a06e19bf5a597405dfeea39fe92aa8c5dd41da73c72c7187755a75f581efb28",
        url="https://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_4.2.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    build_system(
        conditional("cmake", when="@5:"), conditional("generic", when="@:4"), default="cmake"
    )

    requires("build_system=cmake", when="platform=windows")

    variant("pic", default=True, description="Build with position independent code")

    depends_on("blas")
    conflicts(
        "@:5.2.1",
        when="%apple-clang@12:",
        msg="Older SuperLU is incompatible with newer compilers",
    )

    examples_src_dir = "EXAMPLE"

    def test_example(self):
        """build and run test example"""
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.examples_src_dir)
        test_exe = "superlu"
        test_src = f"{test_exe}.c"

        if not os.path.isfile(join_path(test_dir, test_src)):
            raise SkipTest(f"Cached {test_src} is missing")

        with working_dir(test_dir):
            args = []
            if self.version < Version("5.2.2"):
                args.append("HEADER=" + self.prefix.include)
            args.append(test_exe)

            make = which("make")
            make(*args)

            superlu = which(test_exe)
            superlu()


class BaseBuilder(metaclass=spack.builder.PhaseCallbacksMeta):
    @run_after("install")
    def setup_standalone_tests(self):
        """Set up and copy example source files after the package is installed
        to an install test subdirectory for use during `spack test run`."""
        makefile = join_path(self.pkg.examples_src_dir, "Makefile")

        if self.spec.satisfies("@5.2.2:"):
            # Include dir was hardcoded in 5.2.2
            filter_file(
                r"INCLUDEDIR  = -I\.\./SRC", "INCLUDEDIR = -I" + self.prefix.include, makefile
            )

        # Create the example makefile's include file and ensure the new file
        # is the one use.
        filename = "make.inc"
        config_args = []
        if self.spec.satisfies("@5:"):
            lib = "libsuperlu.a"
        else:
            config_args.append("PLAT       = _x86_64")
            lib = f"libsuperlu_{self.spec.version}.a"
        config_args.extend(self._make_hdr_for_test(lib))

        with open(join_path(self.pkg.examples_src_dir, filename), "w") as inc:
            for option in config_args:
                inc.write(f"{option}\n")

        # change the path in the example's Makefile to the file written above
        filter_file(r"include \.\./" + filename, "include ./" + filename, makefile)

        # Cache the examples directory for use by stand-alone tests
        cache_extra_test_sources(self.pkg, self.pkg.examples_src_dir)

    def _make_hdr_for_test(self, lib):
        """Standard configure arguments for make.inc"""
        ranlib = "ranlib" if which("ranlib") else "echo"
        return [
            f"SuperLUroot = {self.prefix}",
            f"SUPERLULIB = {self.prefix.lib}/{lib}",
            f"BLASLIB    = {self.spec['blas'].libs.ld_flags}",
            "TMGLIB     = libtmglib.a",
            "LIBS       = $(SUPERLULIB) $(BLASLIB)",
            "ARCH       = ar",
            "ARCHFLAGS  = cr",
            f"RANLIB     = {ranlib}",
            f"CC         = {env['CC']}",
            f"FORTRAN    = {env['FC']}",
            f"LOADER     = {env['CC']}",
            "CFLAGS     = -O3 -DNDEBUG -DUSE_VENDOR_BLAS -DPRNTlevel=0 -DAdd_",
            "NOOPTS     = -O0",
        ]


class CMakeBuilder(BaseBuilder, spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        if self.pkg.version > Version("5.2.1"):
            _blaslib_key = "enable_internal_blaslib"
        else:
            _blaslib_key = "enable_blaslib"
        args = [
            self.define(_blaslib_key, False),
            self.define("CMAKE_INSTALL_LIBDIR", self.prefix.lib),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define("enable_tests", self.pkg.run_tests),
        ]
        return args


class GenericBuilder(BaseBuilder, spack.build_systems.generic.GenericBuilder):
    def install(self, pkg, spec, prefix):
        """Use autotools before version 5"""
        # Define make.inc file
        config = [
            "PLAT       = _x86_64",
            "SuperLUroot = %s" % self.pkg.stage.source_path,
            # 'SUPERLULIB = $(SuperLUroot)/lib/libsuperlu$(PLAT).a',
            "SUPERLULIB = $(SuperLUroot)/lib/libsuperlu_{0}.a".format(self.pkg.spec.version),
            "BLASDEF    = -DUSE_VENDOR_BLAS",
            "BLASLIB    = {0}".format(spec["blas"].libs.ld_flags),
            # or BLASLIB      = -L/usr/lib64 -lblas
            "TMGLIB     = libtmglib.a",
            "LIBS       = $(SUPERLULIB) $(BLASLIB)",
            "ARCH       = ar",
            "ARCHFLAGS  = cr",
            "RANLIB     = {0}".format("ranlib" if which("ranlib") else "echo"),
            "CC         = {0}".format(env["CC"]),
            "FORTRAN    = {0}".format(env["FC"]),
            "LOADER     = {0}".format(env["CC"]),
            "CDEFS      = -DAdd_",
        ]

        if "+pic" in spec:
            config.extend(
                [
                    # Use these lines instead when pic_flag capability arrives
                    "CFLAGS     = -O3 {0}".format(self.pkg.compiler.cc_pic_flag),
                    "NOOPTS     = {0}".format(self.pkg.compiler.cc_pic_flag),
                    "FFLAGS     = -O2 {0}".format(self.pkg.compiler.f77_pic_flag),
                    "LOADOPTS   = {0}".format(self.pkg.compiler.cc_pic_flag),
                ]
            )
        else:
            config.extend(
                ["CFLAGS     = -O3", "NOOPTS     = ", "FFLAGS     = -O2", "LOADOPTS   = "]
            )

        with open("make.inc", "w") as inc:
            for option in config:
                inc.write("{0}\n".format(option))

        make(parallel=False)

        install_tree("lib", prefix.lib)
        mkdir(prefix.include)
        install(join_path("SRC", "*.h"), prefix.include)
