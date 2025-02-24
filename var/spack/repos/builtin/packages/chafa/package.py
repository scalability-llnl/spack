# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chafa(AutotoolsPackage):
    """A library and command-line utility that converts image data, including
    animated GIFs, into graphics formats or ANSI/Unicode character art
    suitable for display in a terminal."""

    homepage = "https://hpjansson.org/chafa/"
    url = "https://hpjansson.org/chafa/releases/chafa-1.14.5.tar.xz"
    git = "https://github.com/hpjansson/chafa.git"

    license("LGPL-3.0-or-later", checked_by="Buldram")
    maintainers("Buldram")

    version("master", branch="master")
    version("1.14.5", sha256="7b5b384d5fb76a641d00af0626ed2115fb255ea371d9bef11f8500286a7b09e5")
    version("1.14.4", sha256="d0708a63f05b79269dae862a42671e38aece47fbd4fc852904bca51a65954454")
    version("1.14.3", sha256="f3d5530a96c8e55eea180448896e973093e0302f4cbde45d028179af8cfd90f3")
    version("1.14.2", sha256="8a28d308074e25597e21bf280747461ac695ae715f2f327eb0e0f0435967f8b3")
    version("1.14.1", sha256="24707f59e544cec85d7a1993854672136b05271f86954248c5d8a42e221f6f25")
    version("1.14.0", sha256="670e55c28b5ecd4c8187bd97f0898762712a480ec8ea439dae4a4836b178e084")

    variant("shared", default=True, description="Build shared libraries")
    variant("static", default=True, description="Build static libraries")
    variant("tools", default=True, description="Build command-line tool")
    variant("man", default=True, when="@1 +tools", description="Install man page")
    variant("jpeg", default=True, when="+tools", description="Enable JPEG loader")
    variant("tiff", default=False, when="+tools", description="Enable TIFF loader")
    variant("svg", default=False, when="+tools", description="Enable SVG loader")
    variant("webp", default=False, when="+tools", description="Enable WebP loader")
    variant("avif", default=False, when="+tools", description="Enable AVIF loader")
    variant("jxl", default=False, when="@1.14.1: +tools", description="Enable JPEG XL loader")

    conflicts("~shared~static")

    depends_on("c", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libxml2", type="build")
    depends_on("glib", type="link")
    depends_on("freetype", type="link", when="+tools")
    depends_on("jpeg", type="link", when="+jpeg")
    depends_on("libtiff", type="link", when="+tiff")
    depends_on("librsvg", type="link", when="+svg")
    depends_on("libwebp +libwebpdemux", type="link", when="+webp")
    depends_on("libavif", type="link", when="+avif")
    depends_on("libjxl", type="link", when="+jxl")

    @when("@master")
    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")(extra_env={"NOCONFIGURE": "1"})

    def configure_args(self):
        return [
            "--disable-silent-rules",
            "--disable-dependency-tracking",
            "--disable-man",
            *self.enable_or_disable("shared"),
            *self.enable_or_disable("static"),
            *self.with_or_without("tools"),
            *self.with_or_without("jpeg"),
            *self.with_or_without("tiff"),
            *self.with_or_without("svg"),
            *self.with_or_without("webp"),
            *self.with_or_without("avif"),
            *self.with_or_without("jxl"),
        ]

    @run_after("install", when="+man")
    def install_man(self):
        mkdirp(prefix.share.man.man1)
        install("docs/chafa.1", prefix.share.man.man1)
