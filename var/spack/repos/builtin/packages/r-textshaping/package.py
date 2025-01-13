# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTextshaping(RPackage):
    """Bindings to the 'HarfBuzz' and 'Fribidi' Libraries for Text Shaping.

    Provides access to the text shaping functionality in the 'HarfBuzz' library
    and the bidirectional algorithm in the 'Fribidi' library. 'textshaping' is
    a low-level utility package mainly for graphic devices that expands upon
    the font tool-set provided by the 'systemfonts' package."""

    cran = "textshaping"

    license("MIT")

    version("0.4.0", sha256="35e940786bb278560de61bb55d4f46f8c86c878d0461613ceb8c98ba9b239d7a")
    version("0.3.6", sha256="80e2c087962f55ce2811fbc798b09f5638c06c6b28c10cd3cb3827005b902ada")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-cpp11@0.2.1:", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@0.4.0:")
    depends_on("r-systemfonts@1.0.0:", type=("build", "run"))
    depends_on("r-systemfonts@1.1.0:", type=("build", "run"), when="@0.4.0:")
    depends_on("pkgconfig", type="build")
    depends_on("freetype")
    depends_on("harfbuzz")
    depends_on("fribidi")
