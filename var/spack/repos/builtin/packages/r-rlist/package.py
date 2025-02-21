# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRlist(RPackage):
    """Provides a set of functions for data manipulation with
    list objects, including mapping, filtering, grouping, sorting,
    updating, searching, and other useful functions. Most functions
    are designed to be pipeline friendly so that data processing with
    lists can be chained."""

    homepage = "https://renkun-ken.github.io/rlist/"
    cran = "rlist"

    license("MIT", checked_by="wdconinc")

    version("0.4.6.2", sha256="ebde658d897c8a27a90ebb892b9e2bad15e2ad75557a7352fb08cbb5604e0997")

    depends_on("r@2.15:", type=("build", "run"))
    depends_on("r-yaml", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-xml", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"))
