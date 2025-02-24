# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgl(RPackage):
    """3D Visualization Using OpenGL.

    Provides medium to high level functions for 3D interactive graphics,
    including functions modelled on base graphics (plot3d(), etc.) as well as
    functions for constructing representations of geometric objects (cube3d(),
    etc.). Output may be on screen using OpenGL, or to various standard 3D file
    formats including WebGL, PLY, OBJ, STL as well as 2D image formats,
    including PNG, Postscript, SVG, PGF."""

    cran = "rgl"

    license("GPL-2.0-or-later")

    version("1.3.1", sha256="9fea7b59dd7fef9bbd783c745d68325ec753ef412699d168bb6c664a56506d49")
    version("1.1.3", sha256="4fa246c2ab06261ea81e09a7a489f34174b93359fe74a3db291f8d0eccd38aae")
    version("0.110.2", sha256="da1118c1990ae161a5787960fb22009601d2ee7d39ca9c97c31c70589bce346d")
    version("0.108.3.2", sha256="033af3aceade6c21d0a602958fff1c25c21febc7d0e867cf88860cfa25fc3c65")
    version("0.108.3", sha256="89f96eb462cacfcc796ad351d7dac0480a7eb9f80e9bd75e58c5a79f0ee8133b")
    version("0.104.16", sha256="b82d2e2b965e76d6cc55bbd15ee0f79c36913ab09ce5436d2104551563462a99")
    version("0.100.26", sha256="e1889c2723ad458b39fdf9366fdaf590d7657d3762748f8534a8491ef754e740")
    version("0.100.24", sha256="1233a7bdc5a2b908fc64d5f56e92a0e123e8f7c0b9bac93dfd005608b78fa35a")
    version("0.100.19", sha256="50630702554e422e0603f27d499aad3b6f822de5a73da7fdf70404ac50df7025")
    version("0.99.16", sha256="692a545ed2ff0f5e15289338736f0e3c092667574c43ac358d8004901d7a1a61")
    version("0.98.1", sha256="5f49bed9e092e672f73c8a1a5365cdffcda06db0315ac087e95ab9c9c71a6986")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@3.3.0:", type=("build", "run"), when="@0.108.3:")
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.3.1:")
    depends_on("r-htmlwidgets", type=("build", "run"))
    depends_on("r-htmlwidgets@1.6.0:", type=("build", "run"), when="@1.1.3:")
    depends_on("r-htmltools", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"))
    depends_on("r-knitr@1.33:", type=("build", "run"), when="@0.108.3:")
    depends_on("r-jsonlite@0.9.20:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"), when="@0.108.3:")
    depends_on("r-mime", type=("build", "run"), when="@0.110.2:")
    depends_on("r-base64enc", type=("build", "run"), when="@0.110.2:")
    depends_on("libx11")
    depends_on("gl")
    depends_on("glu")
    depends_on("zlib-api", type="link")
    depends_on("libpng@1.2.9:", type="link")
    depends_on("freetype", type="link")
    depends_on("pandoc@1.14:", type="build")

    depends_on("r-shiny", type=("build", "run"), when="@:0.104.16")
    depends_on("r-crosstalk", type=("build", "run"), when="@0.99.16:0.104.16")
    depends_on("r-manipulatewidget@0.9.0:", type=("build", "run"), when="@0.99.16:0.104.16")

    def configure_args(self):
        args = [
            "--x-includes=%s" % self.spec["libx11"].prefix.include,
            "--x-libraries=%s" % self.spec["libx11"].prefix.lib,
            "--with-gl-includes=%s" % self.spec["gl"].headers.directories[0],
            "--with-gl-libraries=%s" % self.spec["gl"].libs.directories[0],
            "--with-gl-prefix=%s" % self.spec["gl"].home,
        ]
        return args
