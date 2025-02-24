# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgrastr(RPackage):
    """Rasterize Layers for 'ggplot2'.

    Rasterize only specific layers of a 'ggplot2' plot while simultaneously
    keeping all labels and text in vector format. This allows users to keep
    plots within the reasonable size limit without loosing vector properties of
    the scale-sensitive information."""

    cran = "ggrastr"

    license("MIT")

    version("1.0.2", sha256="cb27406dca99cea6440adf6edb7eb53141b60322452f5a5d4409e36516ad20d1")
    version("1.0.1", sha256="82d6e90fa38dec85e829f71018532ed5b709a50a585455fc07cb3bae282f5d1f")

    depends_on("r@3.2.2:", type=("build", "run"))
    depends_on("r-ggplot2@2.1.0:", type=("build", "run"))
    depends_on("r-cairo@1.5.9:", type=("build", "run"))
    depends_on("r-ggbeeswarm", type=("build", "run"))
    depends_on("r-png", type=("build", "run"))
    depends_on("r-ragg", type=("build", "run"))
