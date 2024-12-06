# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHms(RPackage):
    """Pretty Time of Day.

    Implements an S3 class for storing and formatting time-of-day values, based
    on the 'difftime' class."""

    cran = "hms"

    license("MIT")

    version("1.1.3", sha256="e626f4c60af46efd53ea631b316a103e089470d8fd63c0e0c0efb99364990282")
    version("1.1.2", sha256="1ee6a9847336aaf58d3fcee5b56c290c2204e1213b6628862818419b2302bded")
    version("1.1.1", sha256="6b5f30db1845c70d27b5de33f31caa487cdd0787cd80a4073375e5f482269062")
    version("1.0.0", sha256="9704e903d724f0911d46e5ad18b469a7ed419c5b1f388bd064fd663cefa6c962")
    version("0.5.0", sha256="a87872665c3bf3901f597d78c152e7805f7129e4dbe27397051de4cf1a76561b")
    version("0.3", sha256="9368259cbc1094ce0e4cf61544875ec30088ef690d6667e6b0b564218ab3ff88")

    depends_on("r-lifecycle", type=("build", "run"), when="@1.0.0:")
    depends_on("r-pkgconfig", type=("build", "run"), when="@0.5.0:")
    depends_on("r-rlang", type=("build", "run"), when="@0.5.0:")
    depends_on("r-rlang@1.0.2:", type=("build", "run"), when="@1.1.3:")
    depends_on("r-vctrs@0.2.0:", type=("build", "run"), when="@0.5.0:")
    depends_on("r-vctrs@0.2.1:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-vctrs@0.3.8:", type=("build", "run"), when="@1.1:")
    depends_on("r-ellipsis", type=("build", "run"), when="@1.0.0:1.1.2")
    depends_on("r-ellipsis@0.3.2", type=("build", "run"), when="@1.1:1.1.2")
    depends_on("r-ellipsis@0.3.2:", type=("build", "run"), when="@1.1.2:1.1.2")
