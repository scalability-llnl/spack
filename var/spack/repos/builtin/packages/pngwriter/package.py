# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pngwriter(CMakePackage):
    """PNGwriter is a very easy to use open source graphics library that uses
    PNG as its output format. The interface has been designed to be as simple
    and intuitive as possible. It supports plotting and reading pixels in the
    RGB (red, green, blue), HSV (hue, saturation, value/brightness) and CMYK
    (cyan, magenta, yellow, black) colour spaces, basic shapes, scaling,
    bilinear interpolation, full TrueType antialiased and rotated text support,
    bezier curves, opening existing PNG images and more.
    """

    homepage = "https://pngwriter.sourceforge.net/"
    url = "https://github.com/pngwriter/pngwriter/archive/0.5.6.tar.gz"
    git = "https://github.com/pngwriter/pngwriter.git"

    maintainers("ax3l")

    version("develop", branch="dev")
    version("master", branch="master")
    version("0.7.0", sha256="82d46eef109f434f95eba9cf5908710ae4e75f575fd3858178ad06e800152825")
    version("0.6.0", sha256="5107c6be0bfadf76ba4d01a553f7e060b5a7763ca7d9374ef3e7e59746b3911e")
    version("0.5.6", sha256="0c5f3c1fd6f2470e88951f4b8add64cf5f5a7e7038115dba69604139359b08f1")

    depends_on("cxx", type="build")  # generated

    depends_on("libpng")
    depends_on("zlib-api")
    depends_on("freetype")

    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("@0.7.0:"):
            args += ["-DPNGwriter_USE_FREETYPE:BOOL=ON"]

        return args
