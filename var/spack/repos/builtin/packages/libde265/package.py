# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libde265(CMakePackage):
    """libde265 is an open source implementation of the h.265 video codec.

    It is written from scratch and has a plain C API to enable
    a simple integration into other software."""

    homepage = "https://www.libde265.org"
    url = "https://github.com/strukturag/libde265/archive/refs/tags/v1.0.9.tar.gz"

    maintainers("benkirk")

    license("LGPL-3.0-or-later")

    version("1.0.15", sha256="d4e55706dfc5b2c5c9702940b675ce2d3e7511025c6894eaddcdbaf0b15fd3f3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.13:", type="build")
