# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Poppler(CMakePackage):
    """Poppler is a PDF rendering library based on the xpdf-3.0 code base."""

    homepage = "https://poppler.freedesktop.org"
    url = "https://poppler.freedesktop.org/poppler-21.09.0.tar.xz"
    list_url = "https://poppler.freedesktop.org/releases.html"
    git = "https://gitlab.freedesktop.org/poppler/poppler.git"

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("23.04.0", sha256="b6d893dc7dcd4138b9e9df59a13c59695e50e80dc5c2cacee0674670693951a1")
    version("21.09.0", sha256="5a47fef738c2b99471f9b459a8bf8b40aefb7eed92caa4861c3798b2e126d05b")
    version("21.07.0", sha256="e26ab29f68065de4d6562f0a3e2b5435a83ca92be573b99a1c81998fa286a4d4")
    version("0.90.1", sha256="984d82e72e91418d280885298c8bdc855a2fd92665fd52a1345b27235e0c71c4")
    version("0.87.0", sha256="6f602b9c24c2d05780be93e7306201012e41459f289b8279a27a79431ad4150e")
    version("0.79.0", sha256="f985a4608fe592d2546d9d37d4182e502ff6b4c42f8db4be0a021a1c369528c8")
    version("0.77.0", sha256="7267eb4cbccd64a58244b8211603c1c1b6bf32c7f6a4ced2642865346102f36b")
    version("0.72.0", sha256="c1747eb8f26e9e753c4001ed951db2896edc1021b6d0f547a0bd2a27c30ada51")
    version("0.65.0", sha256="89c8cf73f83efda78c5a9bd37c28f4593ad0e8a51556dbe39ed81e1ae2dd8f07")
    version("0.64.0", sha256="b21df92ca99f78067785cf2dc8e06deb04726b62389c0ee1f5d8b103c77f64b1")
    version("0.61.1", sha256="1266096343f5163c1a585124e9a6d44474e1345de5cdfe55dc7b47357bcfcda9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("boost", default=False, description="Enable Boost for Splash")
    variant("cms", default=False, description="Use color management system")
    variant("cpp", default=False, description="Compile poppler cpp wrapper")
    variant("glib", default=False, description="Compile poppler glib wrapper")
    variant("gobject", default=False, description="Generate GObject introspection")
    variant("libcurl", default=False, description="Build libcurl based HTTP support")
    variant("openjpeg", default=False, description="Use libopenjpeg for JPX streams")
    variant("qt", default=False, description="Compile poppler qt wrapper")
    variant("zlib", default=False, description="Build with zlib")
    variant("iconv", default=False, description="Search for Iconv package")
    variant("jpeg", default=False, description="Search for JPEG package")
    variant("png", default=False, description="Search for PNG package")
    variant("tiff", default=False, description="Search for TIFF package")

    depends_on("cmake@3.1.0:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("poppler-data", type=("build", "run"))
    depends_on("fontconfig")
    depends_on("freetype")

    depends_on("boost@1.58.0:", when="+boost")
    depends_on("lcms", when="+cms")
    depends_on("glib@2.41:", when="+glib")
    depends_on("gobject-introspection", when="+gobject")
    depends_on("curl", when="+libcurl")
    depends_on("openjpeg", when="+openjpeg")
    depends_on("qt@4.0:", when="+qt")
    depends_on("zlib-api", when="+zlib")
    depends_on("cairo+ft@1.10.0:", when="+glib")
    depends_on("iconv", when="+iconv")
    depends_on("jpeg", when="+jpeg")
    depends_on("libpng", when="+png")
    depends_on("libtiff", when="+tiff")

    depends_on("qt@5.0:", when="@0.62.0:+qt")
    depends_on("qt@4.0:4.8.6", when="@:0.61+qt")

    # Splash is unconditionally disabled. Unfortunately there's
    # a small section of code in the QT5 wrappers that expects it
    # to be present.
    patch("poppler_page_splash.patch", when="@0.64.0:0.90.0 ^qt@5.0:")
    patch("poppler_page_splash.0.90.1.patch", when="@0.90.1:21.06 ^qt@5.0:")

    # Only needed to run `make test`
    resource(
        name="test", git="git://git.freedesktop.org/git/poppler/test.git", placement="testdata"
    )

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DTESTDATADIR={0}".format(join_path(self.stage.source_path, "testdata")),
            # TODO: Add packages for these missing dependencies
            "-DENABLE_SPLASH=OFF",
            "-DWITH_NSS3=OFF",
        ]

        # Install header files
        args.append("-DENABLE_UNSTABLE_API_ABI_HEADERS=ON")

        if "+boost" in spec:
            args.append("-DENABLE_BOOST=ON")
        else:
            args.append("-DENABLE_BOOST=OFF")

        if "+cms" in spec:
            args.append("-DENABLE_CMS=lcms2")
        else:
            args.append("-DENABLE_CMS=none")

        if "+cpp" in spec:
            args.append("-DENABLE_CPP=ON")
        else:
            args.append("-DENABLE_CPP=OFF")

        if "+glib" in spec:
            args.extend(["-DENABLE_GLIB=ON", "-DWITH_GLIB=ON", "-DWITH_Cairo=ON"])
        else:
            args.extend(["-DENABLE_GLIB=OFF", "-DWITH_GLIB=OFF", "-DWITH_Cairo=OFF"])

        if "+gobject" in spec:
            args.append("-DENABLE_GOBJECT_INTROSPECTION=ON")
        else:
            args.append("-DENABLE_GOBJECT_INTROSPECTION=OFF")

        if "+libcurl" in spec:
            args.append("-DENABLE_LIBCURL=ON")
        else:
            args.append("-DENABLE_LIBCURL=OFF")

        if "+openjpeg" in spec:
            args.append("-DENABLE_LIBOPENJPEG=openjpeg2")
        else:
            args.append("-DENABLE_LIBOPENJPEG=none")

        if "+qt" in spec and spec.satisfies("^qt@4.0:4.8.6"):
            args.append("-DENABLE_QT4=ON")
            args.append("-DENABLE_QT5=OFF")
        elif "+qt" in spec and spec.satisfies("^qt@5.0:"):
            args.append("-DENABLE_QT5=ON")
            args.append("-DENABLE_QT4=OFF")
        else:
            args.append("-DENABLE_QT4=OFF")
            args.append("-DENABLE_QT5=OFF")

        if "+zlib" in spec:
            args.append("-DENABLE_ZLIB=ON")
        else:
            args.append("-DENABLE_ZLIB=OFF")

        if "+iconv" in spec:
            args.append("-DWITH_Iconv=ON")
        else:
            args.append("-DWITH_Iconv=OFF")

        if "+jpeg" in spec:
            args.extend(["-DENABLE_DCTDECODER=libjpeg", "-DWITH_JPEG=ON"])
        else:
            args.extend(["-DENABLE_DCTDECODER=none", "-DWITH_JPEG=OFF"])

        if "+png" in spec:
            args.append("-DWITH_PNG=ON")
        else:
            args.append("-DWITH_PNG=OFF")

        if "+tiff" in spec:
            args.append("-DWITH_TIFF=ON")
        else:
            args.append("-DWITH_TIFF=OFF")

        return args
