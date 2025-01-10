# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdegraphics(RPackage):
    """An S4 Lattice-Based Package for the Representation of Multivariate Data.

    Graphical functionalities for the representation of multivariate data.  It
    is a complete re-implementation of the functions available in the 'ade4'
    package."""

    cran = "adegraphics"

    license("GPL-2.0-or-later")

    version("1.0-21", sha256="e02a92b3a03220fd1f905f9541f506e43ad75b385a7febf74c80690364faeba8")
    version("1.0-18", sha256="8fe07fc0f73e9917e098de2ee8e6fdb3e07775446683b6222692a3298e4d563c")
    version("1.0-16", sha256="7ba59ce9aeefe1c25b4b118d08ef458ffd34115412c147cc428629e72a82ec3a")
    version("1.0-15", sha256="87bbcd072e9a898955f5ede4315e82365086a50a2887bf5bd2e94bbb4d3f678a")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r-ade4@1.7-13:", type=("build", "run"))
    depends_on("r-kernsmooth", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-latticeextra", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-sp@1.1-1:", type=("build", "run"))
