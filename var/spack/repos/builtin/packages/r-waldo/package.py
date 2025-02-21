# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWaldo(RPackage):
    """Find Differences Between R Objects.

    Compare complex R objects and reveal the key differences. Designed
    particularly for use in testing packages where being able to quickly
    isolate key differences makes understanding test failures much easier."""

    cran = "waldo"

    license("MIT")

    version("0.5.2", sha256="82cdae1ab2c5e7e5dbf5c6bdf832020b46e152732053fb45de7c9a81afdf2e05")
    version("0.4.0", sha256="57ee89eec9bcbba58cf8fa29c8e097f038768c30833eaf812682826333127eaa")
    version("0.3.1", sha256="ec2c8c1afbc413f8db8b6b0c6970194a875f616ad18e1e72a004bc4497ec019b")
    version("0.2.3", sha256="1fbab22fe9be6ca8caa3df7306c763d7025d81ab6f17b85daaf8bdc8c9455c53")

    depends_on("r@3.6:", type=("build", "run"), when="@0.5.2:")
    depends_on("r-cli", type=("build", "run"))
    depends_on("r-diffobj", type=("build", "run"))
    depends_on("r-diffobj@0.3.4:", type=("build", "run"), when="@0.3.1:")
    depends_on("r-fansi", type=("build", "run"))
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-rematch2", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@0.3.1:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@0.4.0:")
    depends_on("r-tibble", type=("build", "run"))
