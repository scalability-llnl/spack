# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCowplot(RPackage):
    """Streamlined Plot Theme and Plot Annotations for 'ggplot2'.

    Provides various features that help with creating publication-quality
    figures with 'ggplot2', such as a set of themes, functions to align plots
    and arrange them into complex compound figures, and functions that make it
    easy to annotate plots and or mix plots with images. The package was
    originally written for internal use in the Wilke lab, hence the name (Claus
    O. Wilke's plot package). It has also been used extensively in the book
    Fundamentals of Data Visualization."""

    cran = "cowplot"

    license("GPL-2.0-only")

    version("1.1.3", sha256="8756971af5c50381cf00ec7ed622fd5cf3d70f534bdfa3ebadd157b5aef5b273")
    version("1.1.1", sha256="c7dce625b456dffc59ba100c816e16226048d12fdd29a7335dc1f6f6e12eed48")
    version("1.0.0", sha256="70f9a7c46d10f409d1599f1afc9fd3c947051cf2b430f01d903c64ef1e6c98a5")
    version("0.9.3", sha256="3e10475fd7506ea9297ed72eb1a3acf858c6fa99d26e46fc39654eba000c3dcb")
    version("0.9.2", sha256="8b92ce7f92937fde06b0cfb86c7634a39b3b2101e362cc55c4bec6b3fde1d28f")
    version("0.9.1", sha256="953fd9d6ff370472b9f5a9ee867a423bea3e26e406d08a2192ec1872a2e60047")
    version("0.9.0", sha256="d5632f78294c3678c08d3eb090abe1eec5cc9cd15cb5d96f9c43794ead098cb5")
    version("0.8.0", sha256="a617fde25030fe764f20967fb753a953d73b47745a2146c97c2565eb4d06700d")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-ggplot2@2.1.1:", type=("build", "run"))
    depends_on("r-ggplot2@2.2.1:", type=("build", "run"), when="@1.1.1:")
    depends_on("r-ggplot2@3.4.0:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-gtable", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.0.0:")
    depends_on("r-scales", type=("build", "run"))

    depends_on("r-plyr@1.8.2:", type=("build", "run"), when="@:0.9.9")
