# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDiffobj(RPackage):
    """Diffs for R Objects.

    Generate a colorized diff of two R objects for an intuitive visualization
    of their differences."""

    cran = "diffobj"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("0.3.5", sha256="d860a79b1d4c9e369282d7391b539fe89228954854a65ba47181407c53e3cf60")
    version("0.3.3", sha256="414e5573470b9565b9149a0a61c7e8344fb37f889d23dc4e131acc8aa62e6df4")

    depends_on("c", type="build")  # generated

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-crayon@1.3.2:", type=("build", "run"))
