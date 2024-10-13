# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class ScalapackBase(CMakePackage):
    """Base class for building ScaLAPACK, shared with the AMD optimized version
    of the library in the 'amdscalapack' package.
    """

    variant("shared", default=True, description="Build the shared library version")
    variant("pic", default=False, description="Build position independent code")

    provides("scalapack")

    depends_on("mpi")
    depends_on("lapack")
    depends_on("blas")
    depends_on("cmake", when="@2.0.0:", type="build")

    # See: https://github.com/Reference-ScaLAPACK/scalapack/issues/9
    patch("cmake_fortran_mangle.patch", when="@2.0.2:2.0")
    # See: https://github.com/Reference-ScaLAPACK/scalapack/pull/10
    patch("mpi2-compatibility.patch", when="@2.0.2:2.0")
    # See: https://github.com/Reference-ScaLAPACK/scalapack/pull/16
    patch("int_overflow.patch", when="@2.0.0:2.1.0")
    # See: https://github.com/Reference-ScaLAPACK/scalapack/pull/23
    patch("gcc10-compatibility.patch", when="@2.0.0:2.2.0")
    # See: https://github.com/Reference-ScaLAPACK/scalapack/pull/57
    patch(
        "https://github.com/Reference-ScaLAPACK/scalapack/commit/d4d0066c041cf19a23f8b3aa62fbcf5f0a33c166.patch?full_index=1",
        sha256="072b006e485f0ca4cba56096912a986e4d3da73aae51c2205928aa5eb842cefd",
        when="@2.2.0",
    )
    # From Homebrew, integrated @upstream in different form over multiple commits
    patch("fix-build-macos.patch", when="@2.2.0")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%gcc@14:"):
                # https://bugzilla.redhat.com/show_bug.cgi?id=2178710
                flags.append("-std=gnu89")
        elif name == "fflags":
            if self.spec.satisfies("%cce"):
                flags.append("-hnopattern")
        return (flags, None, None)

    @property
    def libs(self):
        # Note that the default will be to search
        # for 'libnetlib-scalapack.<suffix>'
        shared = True if "+shared" in self.spec else False
        return find_libraries("libscalapack", root=self.prefix, shared=shared, recursive=True)

    def cmake_args(self):
        spec = self.spec

        options = [
            "-DBUILD_SHARED_LIBS:BOOL=%s" % ("ON" if "+shared" in spec else "OFF"),
            "-DBUILD_STATIC_LIBS:BOOL=%s" % ("OFF" if "+shared" in spec else "ON"),
        ]

        # Make sure we use Spack's Lapack:
        blas = spec["blas"].libs
        lapack = spec["lapack"].libs
        options.extend(
            [
                "-DLAPACK_FOUND=true",
                "-DLAPACK_INCLUDE_DIRS=%s" % spec["lapack"].prefix.include,
                "-DLAPACK_LIBRARIES=%s" % (lapack.joined(";")),
                "-DBLAS_LIBRARIES=%s" % (blas.joined(";")),
            ]
        )

        c_flags = []
        if "+pic" in spec:
            c_flags.append(self.compiler.cc_pic_flag)
            options.append("-DCMAKE_Fortran_FLAGS=%s" % self.compiler.fc_pic_flag)

        # Work around errors of the form:
        #   error: implicit declaration of function 'BI_smvcopy' is
        #   invalid in C99 [-Werror,-Wimplicit-function-declaration]
        if (
            spec.satisfies("%clang")
            or spec.satisfies("%apple-clang")
            or spec.satisfies("%oneapi")
            or spec.satisfies("%arm")
        ):
            c_flags.append("-Wno-error=implicit-function-declaration")

        options.append(self.define("CMAKE_C_FLAGS", " ".join(c_flags)))

        return options

    @run_after("install")
    def fix_darwin_install(self):
        # The shared libraries are not installed correctly on Darwin:
        if (sys.platform == "darwin") and ("+shared" in self.spec):
            fix_darwin_install_name(self.spec.prefix.lib)


class NetlibScalapack(ScalapackBase):
    """ScaLAPACK is a library of high-performance linear algebra routines for
    parallel distributed memory machines
    """

    homepage = "https://www.netlib.org/scalapack/"
    url = "https://www.netlib.org/scalapack/scalapack-2.0.2.tgz"
    git = "https://github.com/Reference-ScaLAPACK/scalapack"
    tags = ["e4s"]

    license("BSD-3-Clause-Open-MPI")

    version("2.2.0", sha256="40b9406c20735a9a3009d863318cb8d3e496fb073d201c5463df810e01ab2a57")
    version("2.1.0", sha256="61d9216cf81d246944720cfce96255878a3f85dec13b9351f1fa0fd6768220a6")
    version("2.0.2", sha256="0c74aeae690fe5ee4db7926f49c5d0bb69ce09eea75beb915e00bba07530395c")
    version("2.0.1", sha256="a9b34278d4e10b40cbe084c6d87d09af8845e874250719bfbbc497b2a88bfde1")
    version("2.0.0", sha256="e51fbd9c3ef3a0dbd81385b868e2355900148eea689bf915c5383d72daf73114")
    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    # versions before 2.0.0 are not using cmake and requires blacs as
    # a separated package
