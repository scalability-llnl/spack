# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLinprog(RPackage):
    """Linear Programming / Optimization.

    Can be used to solve Linear Programming / Linear Optimization problems by
    using the simplex algorithm."""

    cran = "linprog"

    license("GPL-2.0-or-later")

    version("0.9-4", sha256="81a6aa2fdc075f12dc912794d0554f87705a8b872b99c89a90a69ee9ada864b4")

    depends_on("r@2.4.0:", type=("build", "run"))
    depends_on("r-lpsolve", type=("build", "run"))
