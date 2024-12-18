# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fontconfig(AutotoolsPackage):
    """Fontconfig is a library for configuring/customizing font access"""

    homepage = "https://www.freedesktop.org/wiki/Software/fontconfig/"
    url = "https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.12.3.tar.gz"

    license("MIT")

    version("2.15.0", sha256="f5f359d6332861bd497570848fcb42520964a9e83d5e3abe397b6b6db9bcaaf4")
    version("2.14.2", sha256="3ba2dd92158718acec5caaf1a716043b5aa055c27b081d914af3ccb40dce8a55")
    version("2.13.94", sha256="246d1640a7e54fba697b28e4445f4d9eb63dda1b511d19986249368ee7191882")
    version("2.13.93", sha256="0f302a18ee52dde0793fe38b266bf269dfe6e0c0ae140e30d72c6cca5dc08db5")
    version("2.13.1", sha256="9f0d852b39d75fc655f9f53850eb32555394f36104a044bb2b2fc9e66dbbfa7f")
    version("2.12.3", sha256="ffc3cbf6dd9fcd516ee42f48306a715e66698b238933d6fa7cef02ea8b3b818e")
    version("2.12.1", sha256="a9f42d03949f948a3a4f762287dbc16e53a927c91a07ee64207ebd90a9e5e292")
    version("2.11.1", sha256="b6b066c7dce3f436fdc0dfbae9d36122b38094f4f53bd8dffd45e195b0540d8d")

    depends_on("c", type="build")  # generated

    # freetype2 21.0.15+ provided by freetype 2.8.1+
    depends_on("freetype@2.8.1:", when="@2.13:")
    depends_on("freetype")
    depends_on("gperf", type="build", when="@2.11.1:")
    depends_on("libxml2@2.6:")
    depends_on("pkgconfig@0.9:", type="build")
    depends_on("font-util")
    depends_on("uuid", when="@2.13.1:")
    depends_on("python@3:", type="build", when="@2.13.93:")

    variant("pic", default=False, description="Enable position-independent code (PIC)")

    def patch(self):
        """Make test/run-test.sh compatible with dash"""
        filter_file("SIGINT SIGTERM SIGABRT EXIT", "2 15 6 0", "test/run-test.sh")

    # Resolve known issue with tarballs 2.12.3 - 2.13.0 plus
    # https://gitlab.freedesktop.org/fontconfig/fontconfig/-/issues/10
    @run_before("configure")
    def _rm_offending_header(self):
        force_remove(join_path("src", "fcobjshash.h"))

    def configure_args(self):
        font_path = join_path(self.spec["font-util"].prefix, "share", "fonts")
        args = ["--enable-libxml2", "--disable-docs", f"--with-default-fonts={font_path}"]
        ldflags = []
        libs = []
        deps = []
        if self.spec["bzip2"].satisfies("~shared"):
            deps.append("bzip2")
        if not self.spec["libpng"].satisfies("libs=shared"):
            deps.append("libpng")
        if self.spec["libxml2"].satisfies("~shared"):
            deps.append("libxml-2.0")
        if deps:
            pc = which("pkg-config")
            for lib in deps:
                ldflags.append(pc(lib, "--static", "--libs-only-L", output=str).strip())
                libs.append(pc(lib, "--static", "--libs-only-l", output=str).strip())
            args.append("LDFLAGS=%s" % " ".join(ldflags))
            args.append("LIBS=%s" % " ".join(libs))

        if self.spec.satisfies("+pic"):
            args.append(f"CFLAGS={self.compiler.cc_pic_flag}")
            args.append(f"FFLAGS={self.compiler.f77_pic_flag}")

        return args

    @run_after("install")
    def system_fonts(self):
        # point configuration file to system-install fonts
        # gtk applications were failing to display text without this
        config_file = join_path(self.prefix, "etc", "fonts", "fonts.conf")
        filter_file(
            '<dir prefix="xdg">fonts</dir>',
            '<dir prefix="xdg">fonts</dir><dir>/usr/share/fonts</dir>',
            config_file,
        )
