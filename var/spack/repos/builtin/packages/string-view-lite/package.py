# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from shutil import copytree

from spack.package import *


class StringViewLite(CMakePackage):
    """
    A single-file header-only version of a C++17-like string_view for C++98,
    C++11 and later
    """

    homepage = "https://github.com/martinmoene/string-view-lite"
    url = "https://github.com/martinmoene/string-view-lite/archive/v1.0.0.tar.gz"

    license("BSL-1.0")

    version("1.7.0", sha256="265eaec08c4555259b46f5b03004dbc0f7206384edfac1cd5a837efaa642e01c")
    version("1.2.0", sha256="de5c8be782831bac7e7f9656b7fa185b015ae39fac8123195aeba7cbde019da4")
    version("1.1.0", sha256="88fb33ad7a345a25aca4ddf3244afd81b8d54787e5fb316a7ed60f702bc646cd")
    version("1.0.0", sha256="44e30dedd6f4777e646da26528f9d2d5cc96fd0fa79e2e5c0adc14817d048d63")
    version("0.2.0", sha256="c8ae699dfd2ccd15c5835e9b1d246834135bbb91b82f7fc4211b8ac366bffd34")
    version("0.1.0", sha256="7de87d6595230a6085655dab6145340bc423f2cf206263ef73c9b78f7b153340")

    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        return [
            "-DSTRINGVIEW_LITE_OPT_BUILD_TESTS=%s" % ("ON" if self.run_tests else "OFF"),
            "-DSTRINGVIEW_LITE_OPT_BUILD_EXAMPLES=OFF",
        ]

    # Pre-1.2.0 install was simply a copytree on the includes
    @when("@:1.1")
    def cmake(self, spec, prefix):
        pass

    @when("@:1.1")
    def build(self, spec, prefix):
        pass

    @when("@:1.1")
    def install(self, spec, prefix):
        copytree("include", prefix.include)

    @when("@:1.1")
    def check(self):
        pass
