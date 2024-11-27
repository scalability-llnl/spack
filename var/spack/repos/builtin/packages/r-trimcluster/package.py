# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTrimcluster(RPackage):
    """Cluster analysis with trimming.

    Trimmed k-means clustering. The method is described in Cuesta-Albertos et
    al. (1997) <doi:10.1214/aos/1031833664>."""

    cran = "trimcluster"

    license("GPL-2.0-or-later")

    version("0.1-5", sha256="9239f20e4a06ac2fa89e5d5d89b23a45c8c534a7264d89bede8a35d43dda518b")
    version("0.1-2.1", sha256="b64a872a6c2ad677dfeecc776c9fe5aff3e8bab6bc6a8c86957b5683fd5d2300")
    version("0.1-2", sha256="622fb61580cc19b9061c6ee28ffd751250a127f07904b45a0e1c5438d25b4f53")

    depends_on("r@1.9.0:", type=("build", "run"))
