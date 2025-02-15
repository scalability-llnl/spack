# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxrender(AutotoolsPackage, XorgPackage):
    """libXrender - library for the Render Extension to the X11 protocol."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXrender"
    xorg_mirror_path = "lib/libXrender-0.9.10.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("0.9.12", sha256="0fff64125819c02d1102b6236f3d7d861a07b5216d8eea336c3811d31494ecf7")
    version("0.9.11", sha256="6aec3ca02e4273a8cbabf811ff22106f641438eb194a12c0ae93c7e08474b667")
    version("0.9.10", sha256="770527cce42500790433df84ec3521e8bf095dfe5079454a92236494ab296adf")
    version("0.9.9", sha256="beeac64ff8d225f775019eb7c688782dee9f4cc7b412a65538f8dde7be4e90fe")

    depends_on("c", type="build")

    depends_on("libx11@1.6:")
    # https://gitlab.freedesktop.org/xorg/lib/libxrender/-/merge_requests/14
    conflicts("^libx11@1.8.11:", when="@:0.9.11", msg="libxrender@0.9.12: requires libx11@1.8.11:")

    depends_on("renderproto@0.9:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    @property
    def libs(self):
        return find_libraries("libXrender", self.prefix, shared=True, recursive=True)
