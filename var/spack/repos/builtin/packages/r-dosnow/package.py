# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDosnow(RPackage):
    """Foreach Parallel Adaptor for the 'snow' Package.

    Provides a parallel backend for the %dopar% function using the snow package
    of Tierney, Rossini, Li, and Sevcikova."""

    cran = "doSNOW"

    version("1.0.20", sha256="917cabed166aa2d1ec291691c17e1e3d344e858543e1682e3a442cc0c504bbb8")
    version("1.0.19", sha256="4cd2d080628482f4c6ecab593313d7e42516f5ff13fbf9f90e461fcad0580738")
    version("1.0.18", sha256="70e7bd82186e477e3d1610676d4c6a75258ac08f104ecf0dcc971550ca174766")

    depends_on("r@2.5.0:", type=("build", "run"))
    depends_on("r-foreach@1.2.0:", type=("build", "run"))
    depends_on("r-iterators@1.0.0:", type=("build", "run"))
    depends_on("r-snow@0.3.0:", type=("build", "run"))
