# Copyright 2013-2024 Lawrence Livermore National Security, LLC and otherargs
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Gimp(AutotoolsPackage):
    """GIMP is a cross-platform image editor available for GNU/Linux,
    macOS, Windows and more operating systems. It is free software,
    you can change its source code and distribute your changes.

    Whether you are a graphic designer, photographer, illustrator, or
    scientist, GIMP provides you with sophisticated tools to get your job
    done. You can further enhance your productivity with GIMP thanks to
    many customization options and 3rd party plugins."""

    homepage = "https://www.gimp.org"
    url = "https://download.gimp.org/gimp/v2.10/gimp-2.10.32.tar.bz2"

    maintainers("benkirk")

    conflicts("platform=darwin", msg="spack/GIMP currently requires Linux")
    conflicts("platform=windows", msg="spack/GIMP currently requires Linux")

    license("GPL-3.0-or-later")

    version("2.10.38", sha256="50a845eec11c8831fe8661707950f5b8446e35f30edfb9acf98f85c1133f856e")
    with default_args(deprecated=True):
        version(
            "2.10.32", sha256="3f15c70554af5dcc1b46e6dc68f3d8f0a6cc9fe56b6d78ac08c0fd859ab89a25"
        )
        version(
            "2.10.30", sha256="88815daa76ed7d4277eeb353358bafa116cd2fcd2c861d95b95135c1d52b67dc"
        )
        version(
            "2.10.28", sha256="4f4dc22cff1ab5f026feaa2ab55e05775b3a11e198186b47bdab79cbfa078826"
        )
        version(
            "2.10.26", sha256="5ddbccf1db462a41df9a26197fcb0d24c7152753a36b3c8b8a9506b4136395f7"
        )
        version(
            "2.10.24", sha256="bd1bb762368c0dd3175cf05006812dd676949c3707e21f4e6857435cb435989e"
        )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("doc", default=True, description="Build documentation with gtk-doc")
    variant("ghostscript", default=True, description="Build with ghostscript support")
    variant("jpegxl", default=True, description="Build with JPEG XL image format support")
    # variant(
    #     "libheif",
    #     default=False,
    #     description="Build with the libheif HEIF and AVIF file format decoder and encoder."
    # )
    variant(
        "libmng", default=True, description="Build with Multiple-Image Network Graphics support"
    )
    variant(
        "libwmf",
        default=True,
        description="Build with libwmf Windows Windows Metafile Format (WMF) support",
    )
    variant("libxpm", default=True, description="Build with libxpm support")
    variant("webp", default=True, description="Build with WebP support")
    # variant("python",      default=False, description="Build with Python bindings")

    # ref. https://www.gimp.org/source/
    depends_on("gettext", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("babl")
    depends_on("fontconfig@2.12.4:")
    depends_on("gegl")
    depends_on("gexiv2")
    depends_on("ghostscript", when="+ghostscript")
    depends_on("glib")
    depends_on("glib-networking")
    depends_on("gtk-doc", when="+doc")
    depends_on("gtkplus@2.24.32:2.24.100")
    depends_on("intltool")
    depends_on("jpeg")
    depends_on("libexif")
    # depends_on("libheif+libde265", when="+libheif")
    depends_on("libjxl", when="+jpegxl")
    depends_on("libjxl@:0.7", when="+jpegxl@:2.10.32")
    depends_on("libmng", when="+libmng")
    depends_on("libmypaint@1.4")
    depends_on("libpng")
    depends_on("librsvg")
    depends_on("libtiff")
    depends_on("libwmf", when="+libwmf")
    depends_on("libwebp+libwebpmux+libwebpdemux+libwebpdecoder+gif+jpeg+png+tiff", when="+webp")
    depends_on("libxcursor")
    depends_on("libxpm", when="+libxpm")
    depends_on("mypaint-brushes@1.3")
    depends_on("openexr")
    depends_on("openjpeg")
    # depends_on("python@3.6:", when="+python") # coming in 2.99
    depends_on("pango@1.29.4:")
    depends_on("poppler+glib")
    depends_on("poppler-data@0.4.7:")
    depends_on("zlib-api")

    def url_for_version(self, version):
        # ref: https://download.gimp.org/gimp/v2.10/gimp-2.10.32.tar.bz2"
        url = "https://download.gimp.org/gimp/v{0}/gimp-{1}.tar.bz2"
        return url.format(version.up_to(2), version)

    @when("@:2.10.32")
    def patch(self):
        filter_file("babl ", "babl-0.1 ", "configure")

    def configure_args(self):
        args = [
            "--disable-python",
            "--without-webkit",
            "GIO_USE_TLS=gnutls",
            "GIO_EXTRA_MODULES={0}/lib/gio/modules".format(self.spec["glib-networking"].prefix),
        ]
        if self.spec.satisfies("+libxpm"):
            args.append("--with-libxpm={0}".format(self.spec["libxpm"].prefix))
        return args

    def check(self):
        """All build time checks open windows in the X server, don't do that"""
        pass
