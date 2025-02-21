# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgsci(RPackage):
    """Scientific Journal and Sci-Fi Themed Color Palettes for 'ggplot2'.

    collection of 'ggplot2' color palettes inspired by plots in scientific
    journals, data visualization libraries, science fiction movies, and TV
    shows."""

    cran = "ggsci"

    license("GPL-3.0-or-later")

    version("3.2.0", sha256="41d8ed4c01c3740028bdf2ba9c5550f1142061e4a40c93b1d2160719c59c3c4a")
    version("3.0.0", sha256="8901316516d78f82a2a8685d93ba479424bcfd8cb5e28a28adbd50e68964e129")
    version("2.9", sha256="4af14e6f3657134c115d5ac5e65a2ed74596f9a8437c03255447cd959fe9e33c")
    version("2.8", sha256="b4ce7adce7ef23edf777866086f98e29b2b45b58fed085bbd1ffe6ab52d74ae8")
    version("2.4", sha256="9682c18176fee8e808c68062ec918aaef630d4d833e7a0bd6ae6c63553b56f00")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.0.0:")
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-ggplot2@2.0.0:", type=("build", "run"))
