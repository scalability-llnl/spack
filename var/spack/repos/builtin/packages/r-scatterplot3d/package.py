# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScatterplot3d(RPackage):
    """3D Scatter Plot.

    Plots a three dimensional (3D) point cloud."""

    cran = "scatterplot3d"

    license("GPL-2.0-only")

    version("0.3-44", sha256="1c9c08348c3ed925f59df40cb73accc9e1a169ccfb1e8571f105f40fa98e6ec2")
    version("0.3-43", sha256="90d7bfb535b76008768306ea9209adfb48e0e07f36eabbb59ab6ddb6522f16a5")
    version("0.3-42", sha256="a9fedde70e1a846c4dcafbff20f115425206d507896d12c2b21ff052556c5216")
    version("0.3-41", sha256="4c8326b70a3b2d37126ca806771d71e5e9fe1201cfbe5b0d5a0a83c3d2c75d94")
    version("0.3-40", sha256="8249118aa29199017a6686d8245fed5343dabcf049b1588141a7cf83245b6a29")

    depends_on("r@2.7.0:", type=("build", "run"))
