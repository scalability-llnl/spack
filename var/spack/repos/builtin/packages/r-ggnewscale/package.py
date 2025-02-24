# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgnewscale(RPackage):
    """Multiple Fill and Colour Scales in 'ggplot2'.

    Use multiple fill and colour scales in 'ggplot2'."""

    cran = "ggnewscale"

    license("GPL-3.0-only")

    version("0.5.0", sha256="b7f0dcb38d0e8cb4179d92f38b20489905ceb2a9602b68e2c72997d795c4df2d")
    version("0.4.8", sha256="c7fefa6941ecbc789507e59be13fa96327fe2549681a938c43beb06ca22a9700")

    depends_on("r-ggplot2@3.0.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.5.0:", type=("build", "run"), when="@0.5.0:")
