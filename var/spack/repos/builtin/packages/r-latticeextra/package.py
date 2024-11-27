# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLatticeextra(RPackage):
    """Extra Graphical Utilities Based on Lattice.

    Building on the infrastructure provided by the lattice package, this
    package provides several new high-level functions and methods, as well as
    additional utilities such as panel and axis annotation functions."""

    cran = "latticeExtra"

    version("0.6-30", sha256="c550a76913624818482bf237d48883c58e368ba356ced8ed5e76146672279eed")
    version("0.6-29", sha256="6cadc31d56f73d926e2e8d72e43ae17ac03607a4d1a374719999a4a231e3df11")
    version("0.6-28", sha256="780695323dfadac108fb27000011c734e2927b1e0f069f247d65d27994c67ec2")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@0.6-29:")
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-png", type=("build", "run"), when="@0.6-29:")
    depends_on("r-jpeg", type=("build", "run"), when="@0.6-29:")
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"), when="@0.6-30:")
    depends_on("r-interp", type=("build", "run"), when="@0.6-30:")
