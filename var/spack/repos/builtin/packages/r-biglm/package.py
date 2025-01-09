# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiglm(RPackage):
    """Regression for data too large to fit in memory."""

    homepage = "https://cran.r-project.org/web/packages/biglm/index.html"
    cran = "biglm"

    license("GPL-2.0-or-later", checked_by="wdconinc")

    version("0.9-3", sha256="805d483dc58c041f1616267abeb39cecaaf7271a34e90668a5439383bf9a0d58")

    depends_on("r-dbi", type=("build", "run"))
