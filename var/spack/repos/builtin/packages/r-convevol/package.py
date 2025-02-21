# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RConvevol(RPackage):
    """Analysis of Convergent Evolution.

    Quantifies and assesses the significance of convergent evolution using two
    different methods (and 5 different measures) as described in Stayton (2015)
    <doi:10.1111/evo.12729>. Also displays results in a phylomorphospace
    framework."""

    cran = "convevol"

    license("GPL-2.0-only")

    version("2.2.1", sha256="9b197d8735e61f78825ec2d81380b0f4352a3783c2c51254f4eb415ab45a9b48")
    version("2.0.0", sha256="690664b93c1f144a409e80b2ebfc20dc34f0eb9405607d15e066e8db573e84de")
    version("1.3", sha256="d6b24b9796a559f5280e277746189d141151ade4b14cc6b4c2d9d496d7f314ac")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-geiger", type=("build", "run"))
    depends_on("r-magick", type=("build", "run"), when="@2.2.0:")
    depends_on("r-phytools", type=("build", "run"))

    depends_on("r-mass", type=("build", "run"), when="@:2.1")
