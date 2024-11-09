# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from shutil import copytree

from spack.package import *


class SpanLite(CMakePackage):
    """
    A single-file header-only version of a C++20-like span for C++98, C++11 and
    later
    """

    homepage = "https://github.com/martinmoene/span-lite"
    url = "https://github.com/martinmoene/span-lite/archive/v0.10.3.tar.gz"
    git = "https://github.com/martinmoene/span-lite"

    license("BSL-1.0")

    version("0.11.0", sha256="ef4e028e18ff21044da4b4641ca1bc8a2e2d656e2028322876c0e1b9b6904f9d")
    version("0.10.3", sha256="04ac8148760369f11d4cdbc7969d66cb3d372357b6b5c7744841a60551ccb50b")
    version("0.9.2", sha256="7562802aac9b78e0140c3d59933cf4dc5825c0712c63daad2f7fff8c67e62eb4")
    version("0.8.1", sha256="2136dba54988c16b03f7c652ea977205bf624bfde90c24331177027d6529386d")
    version("0.7.0", sha256="e95a9b281b46eb2b44257c6c4ec218c1741144c1167644896e29fd6aed9bbcf4")
    version("0.5.0", sha256="405ae095bca3c63da28c72a3528369b9ba3996f1992f3ae90fcb01a9d8bdef38")
    version("0.4.0", sha256="973858839cc881f9457a874b9c39e16c3d4a798b1204258bb0ca997cd13d1a87")
    version("0.3.0", sha256="e083f368167fe632f866956edaa2c7a7d57a33ffb0d8def9b9f1a9daa47834bb")
    version("0.2.0", sha256="6e3305fe868442410a00962a39fc59ed494cecc4f99fe2aff187e33932f06e46")
    version("0.1.0", sha256="0a84b9369f86beba326e2160b683fd0922f416ce136437751a9ed70afcc67a1c")

    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        return [
            "-DSPAN_LITE_EXPORT_PACKAGE=ON",
            f"-DSPAN_LITE_OPT_BUILD_TESTS={'ON' if self.run_tests else 'OFF'}",
            "-DSPAN_LITE_OPT_BUILD_EXAMPLES=OFF",
        ]

    # Pre-0.5.0 install was simply a copytree on the includes
    @when("@:0.4")
    def cmake(self, spec, prefix):
        pass

    @when("@:0.4")
    def build(self, spec, prefix):
        pass

    @when("@:0.4")
    def install(self, spec, prefix):
        copytree("include", prefix.include)

    @when("@:0.4")
    def check(self):
        pass
