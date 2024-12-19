# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRlas(RPackage):
    """R package to read and write las and laz files used to store LiDAR data"""

    homepage = "https://cran.r-project.org"
    cran = "rlas"

    maintainers("sidpbury")

    license("LGPL-3.0-only")

    version("1.8.0", sha256="dc7903cfcebcd8c0313e101cae732c8ef7b5839318799c1d3d7b778fa178143b")
    version("1.7.0", sha256="11768b6f21e96905cee6c39eb980b92373afed10ab144bdbab2a7a7602fc6b29")

    depends_on("r@3.6.0:", type=("build", "run"))
    depends_on("parallel", type=("build", "run"))
    depends_on("r-r-utils", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"))
    depends_on("boost@:1.84+filesystem+program_options+numpy+python+regex+serialization+thread")
