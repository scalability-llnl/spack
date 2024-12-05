# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xproto(AutotoolsPackage, XorgPackage):
    """X Window System Core Protocol.

    This package provides the headers and specification documents defining
    the X Window System Core Protocol, Version 11.

    It also includes a number of headers that aren't purely protocol related,
    but are depended upon by many other X Window System packages to provide
    common definitions and porting layer."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/x11proto"
    xorg_mirror_path = "proto/xproto-7.0.31.tar.gz"

    version("7.0.31", sha256="6d755eaae27b45c5cc75529a12855fed5de5969b367ed05003944cf901ed43c7")
    version("7.0.29", sha256="628243b3a0fa9b65eda804810ab7238cb88af92fe89efdbc858f25ee5e93a324")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    def install(self, spec, prefix):
        # Installation fails in parallel
        # See https://github.com/spack/spack/issues/4805
        make("install", parallel=False)
