# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSnowfall(RPackage):
    """Easier cluster computing (based on snow).

    Usability wrapper around snow for easier development of parallel R
    programs. This package offers e.g. extended error checks, and additional
    functions. All functions work in sequential mode, too, if no cluster is
    present or wished. Package is also designed as connector to the cluster
    management tool sfCluster, but can also used without it."""

    cran = "snowfall"

    license("GPL-2.0-or-later")

    version("1.84-6.3", sha256="2641932b01041e34b7afb1261f649755b4c8d6560080e0e2ee549ffdf3b8b143")
    version("1.84-6.2", sha256="9b467ab2b992455c6e1aeabe375c5694761fa1cf8aaf4f003ca47102b656353b")
    version("1.84-6.1", sha256="5c446df3a931e522a8b138cf1fb7ca5815cc82fcf486dbac964dcbc0690e248d")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-snow", type=("build", "run"))
