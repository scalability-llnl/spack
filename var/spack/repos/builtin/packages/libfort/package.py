# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfort(CMakePackage):
    """libfort is a simple crossplatform library to create formatted text tables."""

    homepage = "https://github.com/seleznevae/libfort"
    url = "https://github.com/seleznevae/libfort/archive/refs/tags/v0.4.2.tar.gz"

    license("MIT")

    version("0.4.2", sha256="8f7b03f1aa526e50c9828f09490f3c844b73d5f9ca72493fe81931746f75e489")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("enable_astyle", default=False, description="Enable astyle")
    variant("enable_wchar", default=True, description="Enable wchar support")
    variant("enable_utf8", default=True, description="Enable utf8 support")
    variant("enable_testing", default=True, description="Enables building tests and examples")
    variant("shared", default=False, description="Build shared library")

    depends_on("cmake@3.0.0:", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("FORT_ENABLE_ASTYLE", "enable_astyle"),
            self.define_from_variant("FORT_ENABLE_WCHAR", "enable_wchar"),
            self.define_from_variant("FORT_ENABLE_UTF8", "enable_utf8"),
            self.define_from_variant("FORT_ENABLE_TESTING", "enable_testing"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        return args
