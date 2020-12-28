# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMagick(RPackage):
    """Bindings to 'ImageMagick': the most comprehensive open-source image
    processing library available. Supports many common formats (png, jpeg,
    tiff, pdf, etc) and manipulations (rotate, scale, crop, trim, flip, blur,
    etc). All operations are vectorized via the Magick++ STL meaning they
    operate either on a single frame or a series of frames for working with
    layers, collages, or animation. In RStudio images are automatically
    previewed when printed to the console, resulting in an interactive editing
    environment. The latest version of the package includes a native graphics
    device for creating in-memory graphics or drawing onto images using pixel
    coordinates."""

    homepage = "https://docs.ropensci.org/magick"
    url      = "https://cloud.r-project.org/src/contrib/magick_2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/magick"

    version('2.1', sha256='ef4fb8fc1c5a9cfcc36b22485a0e17d622f61e55803b1e7423fd15f0550de7df')

    depends_on('r-rcpp@0.12.12:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
    depends_on('imagemagick')
