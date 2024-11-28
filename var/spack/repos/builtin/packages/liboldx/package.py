# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liboldx(AutotoolsPackage, XorgPackage):
    """X version 10 backwards compatibility."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/liboldX/"
    xorg_mirror_path = "lib/liboldX-1.0.1.tar.gz"

    version("1.0.1", sha256="74322dbf04df69787485eb24b16e12783dfc3454befaf18482ead51bd7b55dc8")

    depends_on("c", type="build")  # generated

    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
