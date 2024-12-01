# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Muparser(CMakePackage, Package):
    """C++ math expression parser library."""

    homepage = "https://beltoforion.de/en/muparser/"
    url = "https://github.com/beltoforion/muparser/archive/v2.2.5.tar.gz"

    license("BSD-2-Clause")

    version("2.3.4", sha256="0c3fa54a3ebf36dda0ed3e7cd5451c964afbb15102bdbcba08aafb359a290121")
    version("2.2.6.1", sha256="d2562853d972b6ddb07af47ce8a1cdeeb8bb3fa9e8da308746de391db67897b3")
    version("2.2.5", sha256="0666ef55da72c3e356ca85b6a0084d56b05dd740c3c21d26d372085aa2c6e708")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Replace std::auto_ptr by std::unique_ptr
    # https://github.com/beltoforion/muparser/pull/46
    patch("auto_ptr.patch", when="@2.2.5")

    variant("samples", default=True, description="enable samples", when="build_system=cmake")
    variant("openmp", default=True, description="enable OpenMP support", when="build_system=cmake")
    variant(
        "wide_char",
        default=False,
        description="enable wide character strings in place of ASCII",
        when="build_system=cmake",
    )
    variant("shared", default=True, description="enable shared libs", when="build_system=cmake")

    # Non-CMake build system is not supported by windows
    conflicts("platform=windows", when="@:2.2.5")
    build_system(conditional("cmake", when="@2.2.6:"), "generic", default="cmake")

    def cmake_args(self):
        return [
            self.define_from_variant("ENABLE_SAMPLES", "samples"),
            self.define_from_variant("ENABLE_OPENMP", "openmp"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("ENABLE_WIDE_CHAR", "wide_char"),
        ]

    @when("@:2.2.5")
    def install(self, spec, prefix):
        options = [
            "--disable-debug",
            "--disable-samples",
            "--disable-dependency-tracking",
            "CXXFLAGS={0}".format(self.compiler.cxx11_flag),
            "--prefix=%s" % prefix,
        ]

        configure(*options)

        make(parallel=False)
        make("install")
