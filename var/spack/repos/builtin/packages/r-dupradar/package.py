# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDupradar(RPackage):
    """Assessment of duplication rates in RNA-Seq datasets"""

    maintainers("pabloaledo")

    bioc = "dupRadar"

    license("GPL-3.0-only")

    version("1.32.0", commit="7e07fc3a3901f8cae0203759fc24dd7df430a07f")
    version("1.30.3", commit="19e3b13a148c47e69686cd1e872182c564fd4dcd")
    version("1.30.0", commit="3d53d2d2e0c404a25845d78b8df8fee3f6b34eb5")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r-kernsmooth", type=("build", "run"))
    depends_on("r-rsubread", type=("build", "run"))
    depends_on("subread", type=("build", "run"))
