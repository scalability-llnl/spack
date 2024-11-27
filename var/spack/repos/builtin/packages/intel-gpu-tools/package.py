# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class IntelGpuTools(AutotoolsPackage, XorgPackage):
    """Intel GPU Tools is a collection of tools for development and testing of
    the Intel DRM driver. There are many macro-level test suites that get used
    against the driver, including xtest, rendercheck, piglit, and oglconform,
    but failures from those can be difficult to track down to kernel changes,
    and many require complicated build procedures or specific testing
    environments to get useful results. Therefore, Intel GPU Tools includes
    low-level tools and tests specifically for development and testing of the
    Intel DRM Driver."""

    homepage = "https://cgit.freedesktop.org/xorg/app/intel-gpu-tools/"
    xorg_mirror_path = "app/intel-gpu-tools-1.16.tar.gz"

    version("1.20", sha256="c6ee992301e43ec14ef810ef532e2601ecf7399315f942207ae0dd568fd9c2b7")
    version("1.16", sha256="4874e6e7704c8d315deaf5b44cc9467ea5e502c7f816470a4a28827fcb34643f")

    depends_on("c", type="build")  # generated

    depends_on("libdrm@2.4.64:")
    depends_on("libpciaccess@0.10:", when=(sys.platform != "darwin"))
    depends_on("libunwind")
    depends_on("kmod")
    depends_on("cairo@1.12.0:")
    depends_on("glib")

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("python@3:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    def configure_args(self):
        glib_include = join_path(self.spec["glib"].prefix.include, "glib-2.0")
        return ["CPPFLAGS=-I{0}".format(glib_include)]

    # xrandr ?

    # gtk-doc-tools
    # python-docutils
    # x11proto-dri2-dev
    # xutils-dev
