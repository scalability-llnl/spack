# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.cmake
import spack.build_systems.makefile
from spack.package import *


class Plasma(CMakePackage):
    """Parallel Linear Algebra Software for Multicore Architectures, PLASMA is
    a software package for solving problems in dense linear algebra using
    multicore processors and Xeon Phi coprocessors. PLASMA provides
    implementations of state-of-the-art algorithms using cutting-edge task
    scheduling techniques. PLASMA currently offers a collection of routines for
    solving linear systems of equations, least squares problems, eigenvalue
    problems, and singular value problems."""

    homepage = "https://github.com/icl-utk-edu/plasma/"
    url = "https://github.com/icl-utk-edu/plasma/releases/download/21.8.29/plasma-21.8.29.tar.gz"
    git = "https://github.com/icl-utk-edu/plasma"

    maintainers("luszczek")

    tags = ["e4s"]

    license("BSD-3-Clause")

    version("develop", git=git)
    version("24.8.7", sha256="748464deb08642d2ea7309fb667e1383d85127c2cd8f0d134180b39c17834503")
    version("23.8.2", sha256="2db34de0575f3e3d16531bdcf1caddef146f68e71335977a3e8ec193003ab943")
    version("22.9.29", sha256="78827898b7e3830eee2e388823b9180858279f77c5eda5aa1be173765c53ade5")
    version("21.8.29", sha256="e0bb4d9143c8540f9f46cbccac9ed0cbea12500a864e6954fce2fe94ea057a10")
    version("20.9.20", sha256="2144a77b739f8dd2f0dbe5b64d94cde0e916f55c4eb170facd168c0db7fc7970")
    version("19.8.1", sha256="3a5db6eabf91aec782b7f27b17a7f6b8ce2c9d8e648c0e9c0ff5d87277ba4d17")
    version("19.8.0", sha256="19a950ade8a7c8d082f372789c9f874274a63217ecff26e33f366402f060f071")
    version("18.11.1", sha256="0581cc8b1188932fd9c29bd258ffe2dc8fb26b1530c5dc3d91f8de369e44edbc")
    version("18.11.0", sha256="36501488be5b4b2b973524824e1afd27779d37addfeeb34c1871ba753b6c06bf")
    version("18.10.0", sha256="93dceae93f57a2fbd79b85d2fbf7907d1d32e158b8d1d93892d9ff3df9963210")
    version("18.9.0", sha256="753eae28ea48986a2cc7b8204d6eef646584541e59d42c3c94fa9879116b0774")
    version(
        "17.1",
        sha256="d4b89f7c3d240a69dfe986284a14471eec4830b9e352ae902ea8861f15573dee",
        url="https://github.com/icl-utk-edu/plasma/releases/download/17.01/plasma-17.01.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    build_system(
        conditional("makefile", when="@:17.1"),
        conditional("cmake", when="@18.9:"),
        default="cmake",
    )

    variant("shared", default=True, description="Build shared library (disables static library)")
    variant("lua", default=False, description="Build Lua support for tuning tile sizes")

    # need a Python version to generate all precisions' code in repo
    depends_on("python", when="@develop", type="build")

    depends_on("lua", when="+lua")

    depends_on("blas")
    depends_on("lapack")

    conflicts("^atlas")  # does not have LAPACKE interface

    # missing LAPACKE features and/or CBLAS headers
    conflicts("^netlib-lapack@:3.5")

    # clashes with OpenBLAS declarations and has a problem compiling on its own
    conflicts("^veclibfort")

    # only GCC 4.9+ and higher have sufficient support for OpenMP 4+ tasks+deps
    conflicts("%gcc@:4.8", when="@:17.1")
    # only GCC 6.0+ and higher have for OpenMP 4+ Clause "priority"
    conflicts("%gcc@:5", when="@17.2:")

    conflicts("%cce")
    conflicts("%apple-clang")
    conflicts("%clang")
    conflicts("%intel")
    conflicts("%nag")
    conflicts("%pgi")
    conflicts("%xl")
    conflicts("%xl_r")

    patch("remove_absolute_mkl_include.patch", when="@17.1")
    patch("protect_cmake_version.patch", when="@19.8.0:19.8.9")
    patch("fix_cmake_include.patch", when="@19.8.0:19.8.9")

    @when("@22.9.29")
    def patch(self):
        filter_file(
            "^(#define PLASMA_CORE_LAPACK_H)$",
            '\\1\n\n#include "plasma_config.h"',
            "include/core_lapack.h",
        )

    @when("@develop:")
    def patch(self):
        python("tools/generate_precisions.py")


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        options = [
            self.define("BLAS_LIBRARIES", self.spec["blas"].libs.joined(";")),
            self.define("LAPACK_LIBRARIES", self.spec["lapack"].libs.joined(";")),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("PLASMA_DETECT_LUA", "lua"),
        ]

        for package, provider in (
            ("openblas", "openblas"),
            ("intel-mkl", "mkl"),
            ("netlib-lapack", "netlib"),
        ):
            if package in self.spec:
                for lib in ("CBLAS", "LAPACKE"):
                    options.append(self.define("{}_PROVIDER".format(lib), provider))
        if "cray-libsci" in self.spec:
            for lib in ("CBLAS", "LAPACKE"):
                libsci_prefix = self.spec["cray-libsci"].package.external_prefix
                options.append(self.define("{}_PROVIDER".format(lib), "generic"))
                options.append(
                    self.define("{}_INCLUDE_DIRS".format(lib), join_path(libsci_prefix, "include"))
                )
                options.append(
                    self.define("{}_LIBRARIES".format(lib), self.spec["blas"].libs.joined(";"))
                )
            options.append(self.define("CBLAS_ADD_TYPEDEF", True))

        return options


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    def edit(self, pkg, spec, prefix):
        # copy "make.inc.mkl-gcc" provided by default into "make.inc"
        open("make.inc", "w").write(open("make.inc.mkl-gcc").read())

        make_inc = FileFilter("make.inc")

        if not spec.satisfies("^intel-mkl"):
            make_inc.filter("-DPLASMA_WITH_MKL", "")  # not using MKL
            make_inc.filter("LIBS *= *.*", "LIBS = " + self.spec["blas"].libs.ld_flags + " -lm")

        header_flags = ""
        # accumulate CPP flags for headers: <cblas.h> and <lapacke.h>
        for dep in ("blas", "lapack"):
            try:  # in case the dependency does not provide header flags
                header_flags += " " + spec[dep].headers.cpp_flags
            except AttributeError:
                pass

        make_inc.filter("CFLAGS +[+]=", "CFLAGS += " + header_flags + " ")

        # pass prefix variable from "make.inc" to "Makefile"
        make_inc.filter("# --*", "prefix={0}".format(self.prefix))

        # make sure CC variable comes from build environment
        make_inc.filter("CC *[?]*= * .*cc", "")
