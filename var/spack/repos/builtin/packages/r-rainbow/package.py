# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRainbow(RPackage):
    """Bagplots, Boxplots and Rainbow Plots for Functional Data.

    Visualizing functional data and identifying functional outliers."""

    cran = "rainbow"

    license("GPL-3.0-only")

    version("3.8", sha256="eca456288b70fe4b6c74a587d8624d3b36d67f8f9ffc13320eefb17a952d823d")
    version("3.7", sha256="159dd90555eee237397f042d811f773aaee779f5036c4e0669a52c36e28d8db2")
    version("3.6", sha256="63d1246f88a498f3db0321b46a552163631b288a25b24400935db41326636e87")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@3.7:")
    depends_on("r-pcapp", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-hdrcde", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-colorspace", type=("build", "run"))
    depends_on("r-ks", type=("build", "run"))
