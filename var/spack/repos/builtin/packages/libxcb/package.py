# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxcb(AutotoolsPackage, XorgPackage):
    """The X protocol C-language Binding (XCB) is a replacement
    for Xlib featuring a small footprint, latency hiding, direct
    access to the protocol, improved threading support, and
    extensibility."""

    homepage = "https://xcb.freedesktop.org/"
    xorg_mirror_path = "lib/libxcb-1.14.tar.xz"

    license("MIT")

    maintainers("wdconinc")

    version("1.17.0", sha256="599ebf9996710fea71622e6e184f3a8ad5b43d0e5fa8c4e407123c88a59a6d55")
    version("1.16.1", sha256="f24d187154c8e027b358fc7cb6588e35e33e6a92f11c668fe77396a7ae66e311")
    version("1.16", sha256="4348566aa0fbf196db5e0a576321c65966189210cb51328ea2bb2be39c711d71")
    version("1.15", sha256="cc38744f817cf6814c847e2df37fcb8997357d72fa4bcbc228ae0fe47219a059")
    version("1.14", sha256="a55ed6db98d43469801262d81dc2572ed124edc3db31059d4e9916eb9f844c34")
    version(
        "1.13",
        sha256="0bb3cfd46dbd90066bf4d7de3cad73ec1024c7325a4a0cbf5f4a0d4fa91155fb",
        url="https://xcb.freedesktop.org/dist/libxcb-1.13.tar.gz",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("libpthread-stubs")
    depends_on("libxau@0.99.2:")
    depends_on("libxdmcp")

    # libxcb 1.X requires xcb-proto >= 1.X
    depends_on("xcb-proto", type="build")
    depends_on("xcb-proto@1.17:", when="@1.17", type="build")
    depends_on("xcb-proto@1.16:", when="@1.16", type="build")
    depends_on("xcb-proto@1.15:", when="@1.15", type="build")
    depends_on("xcb-proto@1.14:", when="@1.14", type="build")
    depends_on("xcb-proto@1.13:", when="@1.13", type="build")

    depends_on("python", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    def configure_args(self):
        config_args = []

        # -Werror flags are not properly interpreted by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc@:20.11"):
            config_args.append("--disable-selective-werror")

        return config_args

    def patch(self):
        filter_file("typedef struct xcb_auth_info_t {", "typedef struct {", "src/xcb.h")

    # libxcb fails to build with non-UTF-8 locales, see:
    # https://www.linuxfromscratch.org/blfs/view/git/x/libxcb.html
    # https://gitlab.freedesktop.org/xorg/lib/libxcb/-/merge_requests/53 (merged in 1.17.0)
    # https://gitlab.freedesktop.org/xorg/lib/libxcb/-/merge_requests/60
    # If a newer release can be verified to build with LC_ALL=en_US.ISO-8859-1,
    # then we can limit the following function, e.g.
    # when("@:1.17")
    def setup_build_environment(self, env):
        env.set("LC_ALL", "C.UTF-8")
