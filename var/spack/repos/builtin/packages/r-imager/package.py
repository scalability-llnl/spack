# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RImager(RPackage):
    """Image Processing Library Based on 'CImg'.

    Fast image processing for images in up to 4 dimensions (two spatial
    dimensions, one time/depth dimension, one colour dimension). Provides most
    traditional image processing tools (filtering, morphology, transformations,
    etc.) as well as various functions for easily analysing image data using R.
    The package wraps 'CImg', <https://cimg.eu/>, a simple, modern C++ library
    for image processing."""

    cran = "imager"

    license("LGPL-3.0-only")

    version("1.0.2", sha256="7c849086cb17d6c5aefc106217363e14afbcda2a9e0120687d40805b5e1c566a")
    version("0.42.19", sha256="187abccba648ecece5e466ca6333acd5c8fdd1476daa2d04d5fa9ec5400ae1e2")
    version("0.42.13", sha256="d90a9893d11190ba249c7fae5bd6517a77907efbce2941452cb2aec57bb5cf7f")
    version("0.42.11", sha256="47f8b7ff8d05a5191e30ad1869f12a62bdbe3142b22b12a6032dec9b5f8532a8")
    version("0.42.10", sha256="01939eb03ad2e1369a4240a128c3b246a4c56f572f1ea4967f1acdc555adaeee")
    version("0.42.3", sha256="6fc308153df8251cef48f1e13978abd5d29ec85046fbe0b27c428801d05ebbf3")
    version("0.41.2", sha256="9be8bc8b3190d469fcb2883045a404d3b496a0380f887ee3caea11f0a07cd8a5")

    depends_on("r+X")
    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-rcpp@0.11.5:", type=("build", "run"))
    depends_on("r-rcpp@1.0.0:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-png", type=("build", "run"))
    depends_on("r-jpeg", type=("build", "run"))
    depends_on("r-readbitmap", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-downloader", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"))
    depends_on("fftw")
    depends_on("libtiff")

    depends_on("r-cairo", type=("build", "run"), when="@:0.41.2")
    depends_on("r-plyr", type=("build", "run"), when="@:0.41.2")
