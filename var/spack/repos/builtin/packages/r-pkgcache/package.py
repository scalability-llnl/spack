# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPkgcache(RPackage):
    """Cache 'CRAN'-Like Metadata and R Packages.

    Metadata and package cache for CRAN-like repositories. This is a utility
    package to be used by package management tools that want to take advantage
    of caching."""

    cran = "pkgcache"

    license("MIT")

    version("2.2.2", sha256="7ebd6cc5fc0325eae504877dfe9651f90e51b3b9778cecc8aae2671b617b5be3")
    version("2.1.0", sha256="cfc03c2060028097972c32c3f2d922d7a598dfd963e5e5250d85a3dfa2f2e206")
    version("2.0.3", sha256="80deafd60f15dda029536d4ce13c37ef91c49cb6636323daadbf3d64a67da028")
    version("2.0.2", sha256="6860b5b7046ef349c2fdad4ba3aecb57c7516fba952a19e3ff7cccb7f859f881")
    version("2.0.1", sha256="1add648c6f30543cbd5e43369c4d1462248d4caaedfcb588ee7b946a75d42f4f")
    version("1.3.0", sha256="bd5f460a3bee9fc1298cf9f747bc59a6b9fbed90e92454bc6ea6bf82c15b9471")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@2.0.2:")
    depends_on("r-callr@2.0.4.9000:", type=("build", "run"))
    depends_on("r-cli@2.0.0:", type=("build", "run"))
    depends_on("r-cli@3.2.0:", type=("build", "run"), when="@2.0.1:")
    depends_on("r-curl@3.2:", type=("build", "run"))
    depends_on("r-filelock", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-processx@3.3.0.9001:", type=("build", "run"))

    depends_on("r-assertthat", type=("build", "run"), when="@:1.3.0")
    depends_on("r-digest", type=("build", "run"), when="@:1.3.0")
    depends_on("r-rlang", type=("build", "run"), when="@:1.3.0")
    depends_on("r-tibble", type=("build", "run"), when="@:1.3.0")
    depends_on("r-uuid", type=("build", "run"), when="@:1.3.0")
    depends_on("r-glue", type=("build", "run"), when="@:2.0.2")
    depends_on("r-prettyunits", type=("build", "run"), when="@:2.2.0")
    depends_on("r-rappdirs", type=("build", "run"), when="@:2.2.0")
