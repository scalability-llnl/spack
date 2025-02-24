# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeomorph(RPackage):
    """Geometric Morphometric Analyses of 2D/3D Landmark Data.

    Read, manipulate, and digitize landmark data, generate shape variables via
    Procrustes analysis for points, curves and surfaces, perform shape
    analyses, and provide graphical depictions of shapes and patterns of shape
    variation."""

    cran = "geomorph"

    license("GPL-3.0-or-later")

    version("4.0.8", sha256="14b4ad5a03fb58d9e7d02ddc4d0756553e9480ded3e68fd699249d58870f0c55")
    version("4.0.5", sha256="900d41f95a610b026763797f290ce94c10827a59b05030ed01c841c59264313b")
    version("4.0.4", sha256="dfded29070bc06bf1dc0d6fedaa16fea9f8eef76f0a7443a11f2835c328c6b0a")
    version("4.0.3", sha256="8fd77bedf2ee85f1e4aaac4b22253810d12dba0b79d78d67695d237b7184e263")
    version("4.0.1", sha256="9d54fba96dd8b8f2dcc8d0e4c427f6232bed1934da41f25084c16ec0b2c71117")
    version("3.3.2", sha256="5f1d17cb98c54e40c4bbc650f7ccb5cb26e8d63934f810644facc69e91c1b7b7")
    version("3.1.2", sha256="29cf1c484f756cb44808cfdbc20137a6fbc4bd0c5c6f98c6c3f397c5aebda8f1")
    version("3.1.1", sha256="8eb222011433100860b308beef6f02ade7c421785f575ab4461ee25e38dfa1bd")
    version("3.0.7", sha256="68f8942e1a5bc3f0298c9f5b8f69c4702c8e12ecb2275d740fda4d04d66d38e1")
    version("3.0.5", sha256="7a3a587b253770a5e7e70536234dee13e6a073f1fdf1d644ae4f11d2eb95b104")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.3.2:")
    depends_on("r@4.4.0:", type=("build", "run"), when="@4.0.8:")
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rrpp", type=("build", "run"), when="@3.0.7:")
    depends_on("r-rrpp@1.0.0:", type=("build", "run"), when="@4.0.1:")
    depends_on("r-rrpp@2.0.1:", type=("build", "run"), when="@4.0.8:")
    depends_on("r-rgl", type=("build", "run"))
    depends_on("r-jpeg", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"), when="@4.0.1:")

    depends_on("r-geiger", type=("build", "run"), when="@:3.1.1")
