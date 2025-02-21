# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMagick(RPackage):
    """Advanced Graphics and Image-Processing in R.

    Bindings to 'ImageMagick': the most comprehensive open-source image
    processing library available. Supports many common formats (png, jpeg,
    tiff, pdf, etc) and manipulations (rotate, scale, crop, trim, flip, blur,
    etc). All operations are vectorized via the Magick++ STL meaning they
    operate either on a single frame or a series of frames for working with
    layers, collages, or animation. In RStudio images are automatically
    previewed when printed to the console, resulting in an interactive editing
    environment. The latest version of the package includes a native graphics
    device for creating in-memory graphics or drawing onto images using pixel
    coordinates."""

    cran = "magick"

    license("MIT")

    version("2.8.4", sha256="45c803370f0d96b729db8114b3e2187cbe6fac13133b67b96a91c8eae734ea0a")
    version("2.7.4", sha256="e28d67737590f8c19e4cf00a9c74e59d0e45f9ece363ed105b5f40e821e8f02f")
    version("2.7.3", sha256="83877b2e23ea43fbc1164de9c2422eafbe7858393ac384df5adf3a7eec122441")
    version("2.6.0", sha256="66585336e3ff18793ae9e2726af67a6672622f270468670ab5fe5e013bc48ecc")
    version("2.1", sha256="ef4fb8fc1c5a9cfcc36b22485a0e17d622f61e55803b1e7423fd15f0550de7df")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-rcpp@0.12.12:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-curl", type=("build", "run"))
    depends_on("imagemagick")
