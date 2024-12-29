# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Imagemagick(AutotoolsPackage):
    """ImageMagick is a software suite to create, edit, compose,
    or convert bitmap images."""

    homepage = "https://www.imagemagick.org"
    url = "https://github.com/ImageMagick/ImageMagick/archive/7.0.2-7.tar.gz"

    license("ImageMagick")

    version("7.1.1-39", sha256="b2eb652d9221bdeb65772503891d8bfcfc36b3b1a2c9bb35b9d247a08965fd5d")
    version("7.1.1-29", sha256="27bd25f945efdd7e38f6f9845a7c0a391fdb732f652dda140b743769c5f106e8")
    version("7.1.1-11", sha256="98bb2783da7d5b06e7543529bd07b50d034fba611ff15e8817a0f4f73957d934")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2023-34153
        version(
            "7.1.0-62", sha256="d282117bc6d0e91ad1ad685d096623b96ed8e229f911c891d83277b350ef884a"
        )
        version(
            "7.1.0-60", sha256="94424cc13c5ba18e0e5d5badb834ce74eab11207b00ea32c1f533a5e34c85887"
        )
        version(
            "7.0.11-14", sha256="dfa5aa3f7f289f12c2f9ee6c7c19b02ae857b4eec02f40298f60f5c11048a016"
        )
        version(
            "7.0.10-62", sha256="84442158aea070095efa832cfe868fd99d6befdf609444f0c9e9f1b4f25480cd"
        )
        version(
            "7.0.9-27", sha256="aeea7768bf330d87efa80fa89f03c5acc2382eae32d1d871acb813e5b116395a"
        )
        version(
            "7.0.8-7", sha256="fadb36b59f310e9eee5249ecb2326b323a64da6cc716dd6d08ece8ea2c780b81"
        )
        version(
            "7.0.5-9", sha256="b85b269e0ed1628e88e840053823f8a33c314b2271f04762f43d33e9d0b4d264"
        )
        version(
            "7.0.2-7", sha256="f2f18a97f861c1668befdaff0cc3aaafb2111847aab028a88b4c2cb017acfbaa"
        )
        version(
            "7.0.2-6", sha256="7d49ca8030f895c683cae69c52d8edfc4876de651f5b8bfdbea907e222480bd3"
        )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("ghostscript", default=False, description="Compile with Ghostscript support")
    variant("rsvg", default=False, description="Enable RSVG support")

    depends_on("pkgconfig@0.20:", type="build")

    depends_on("fontconfig@2.1:")
    depends_on("freetype@2.8:")
    depends_on("jpeg")
    depends_on("pango@1.28.1:")
    depends_on("libpng@1:")
    depends_on("librsvg@2.9:", when="+rsvg")
    depends_on("libtiff@4:")
    depends_on("ghostscript", when="+ghostscript")
    depends_on("ghostscript-fonts", when="+ghostscript")

    depends_on("libsm", when="@:7.1.0-60 platform=linux")

    def configure_args(self):
        args = []
        spec = self.spec
        if spec.satisfies("+ghostscript"):
            args.append("--with-gslib")
            gs_font_dir = spec["ghostscript-fonts"].prefix.share.font
            args.append("--with-gs-font-dir={0}".format(gs_font_dir))
        else:
            args.append("--without-gslib")
        args.extend(self.with_or_without("rsvg"))
        return args

    @property
    def libs(self):
        return find_libraries("libMagick*", root=self.prefix, recursive=True)
