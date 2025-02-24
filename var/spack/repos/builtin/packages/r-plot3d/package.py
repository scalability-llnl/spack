# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPlot3d(RPackage):
    """Plotting Multi-Dimensional Data.

    Functions for viewing 2-D and 3-D data, including perspective plots, slice
    plots, surface plots, scatter plots, etc. Includes data sets from
    oceanography."""

    cran = "plot3D"

    version("1.4.1", sha256="db6df74844dda9177f2be024762b2f0e63182916e987a09480514d078d55d1f4")
    version("1.4", sha256="d04a45197646fb36bc38870c1c2351cb56b912bd772b1ebfa25eaeef35fda9c0")
    version("1.3", sha256="b9e4ec2789e34ad249318900e186868650e1a33466b385cb492a45466db3dfc9")
    version("1.1.1", sha256="f6fe4a001387132626fc553ed1d5720d448b8064eb5a6917458a798e1d381632")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@2.15:", type=("build", "run"))
    depends_on("r-misc3d", type=("build", "run"))
