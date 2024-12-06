# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCircstats(RPackage):
    """Circular Statistics, from "Topics in Circular Statistics" (2001).

    Circular Statistics, from "Topics in Circular Statistics" (2001) S.  Rao
    Jammalamadaka and A. SenGupta, World Scientific."""

    cran = "CircStats"

    maintainers("dorton21")

    license("GPL-2.0-only")

    version("0.2-6", sha256="8efed93b75b314577341effea214e3dd6e0a515cfe1212eb051047a1f3276f1d")

    depends_on("r-mass", type=("build", "run"))
    depends_on("r-boot", type=("build", "run"))
