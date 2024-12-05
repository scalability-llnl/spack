# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Imake(AutotoolsPackage, XorgPackage):
    """The imake build system."""

    homepage = "https://gitlab.freedesktop.org/xorg/util/imake"
    xorg_mirror_path = "util/imake-1.0.7.tar.gz"

    license("custom")

    version("1.0.10", sha256="9bbe76b6bb39caf34a437f50010f58a13d7dd6d512e00e765a2b7883e6ae613c")
    version("1.0.9", sha256="ca53ad18c683091490596d72fee8dbee4c6ddb7693709e25f26da140d29687c1")
    version("1.0.7", sha256="6bda266a07eb33445d513f1e3c82a61e4822ccb94d420643d58e1be5f881e5cb")

    depends_on("c", type="build")

    depends_on("xproto", type="build")
    depends_on("xorg-cf-files", type="run")
    depends_on("pkgconfig", type="build")

    def configure_args(self):
        args = []
        cfgdir = self.spec["xorg-cf-files"].prefix.lib.X11.config
        args.append(f"--with-config-dir={cfgdir}")
        return args
