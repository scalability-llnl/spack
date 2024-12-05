# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAutomap(RPackage):
    """Automatic Interpolation Package.

    An automatic interpolation is done by automatically estimating the
    variogram and then calling gstat. An overview is given by Hiemstra et al
    (2008) <doi:10.1016/j.cageo.2008.10.011>."""

    cran = "automap"

    license("GPL-2.0-or-later")

    version("1.1-9", sha256="f3070aed385352d2595ceddd74cb03cd71965f2e60b675832d16ec2ead6f3a43")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-gstat", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-reshape", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-sp", type=("build", "run"))
    depends_on("r-sf", type=("build", "run"))
    depends_on("r-stars", type=("build", "run"))
