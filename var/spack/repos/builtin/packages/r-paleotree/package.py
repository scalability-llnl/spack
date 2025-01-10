# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RPaleotree(RPackage):
    """Paleontological and Phylogenetic Analyses of Evolution.

    Provides tools for transforming, a posteriori time-scaling, and modifying
    phylogenies containing extinct (i.e. fossil) lineages"""

    cran = "paleotree"

    license("CC0-1.0")

    version("3.4.7", sha256="cb28c8a7929905b50094439423b7839174f7ae1b652607583528d44e102f6317")
    version("3.4.5", sha256="c4dceb3352b74730643aa9f62ceb7f020ce6763614ba334723aadf0eb003d125")
    version("3.4.4", sha256="8809c3395e6904669db8c7cc3b54dd5c3c76948c8568d310cf02e4a5dbc678e4")
    version("3.3.25", sha256="aa64b9120075581229439227a12db776d052b03eb5f9721692a16a9402ac8712")
    version("3.3.0", sha256="f8f6b0228dd5290b251cad3a8626689442b5aa793d8f072c8c2c7813a063df90")
    version("3.1.3", sha256="4c1cc8a5e171cbbbd88f78914f86d5e6d144ae573816fbeeff2ab54a814ec614")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@4.1.0:", type=("build", "run"), when="@3.4.4:")
    depends_on("r-ape@4.1:", type=("build", "run"))
    depends_on("r-phangorn@2.0.0:", type=("build", "run"))
    depends_on("r-phangorn@2.6.3:", type=("build", "run"), when="@3.4.4:")
    depends_on("r-phytools@0.6-00:", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"), when="@3.3.0:")
    depends_on("r-png", type=("build", "run"), when="@3.3.0:")
    depends_on("r-rcurl", type=("build", "run"), when="@3.3.0:")
