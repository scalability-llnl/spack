# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDupradar(RPackage):
    """Assessment of duplication rates in RNA-Seq datasets"""

    maintainers("pabloaledo")

    bioc = "dupRadar"

    license("GPL-3.0-only")

    version("1.37.0", commit="9afe62b26fc33a14cdd2f41f27f05a872201abf7")
    version("1.32.0", commit="7e07fc3a3901f8cae0203759fc24dd7df430a07f")
    version("1.30.3", commit="19e3b13a148c47e69686cd1e872182c564fd4dcd")
    version("1.30.0", commit="3d53d2d2e0c404a25845d78b8df8fee3f6b34eb5")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-kernsmooth", type=("build", "run"))
    depends_on("r-rsubread@1.14.1:", type=("build", "run"))
    depends_on("subread", type=("build", "run"))
