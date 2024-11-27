# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSdmtools(RPackage):
    """Species Distribution Modelling Tools: Tools for processing data
    associated with species distribution modelling exercises.

    This packages provides a set of tools for post processing the outcomes of
    species distribution modeling exercises. It includes novel methods for
    comparing models and tracking changes in distributions through time. It
    further includes methods for visualizing outcomes, selecting thresholds,
    calculating measures of accuracy and landscape fragmentation statistics,
    etc.. This package was made possible in part by financial support from the
    Australian Research Council & ARC Research Network for Earth System
    Science."""

    cran = "SDMTools"

    # This package was removed from CRAN on 2020-01-12
    # The spack recipe contains the latest version available from the archives
    version("1.1-221.2", sha256="f0dd8c5f98d2f2c012536fa56d8f7a58aaf0c11cbe3527e66d4ee3194f6a6cf7")
    version("1.1-221.1", sha256="3825856263bdb648ca018b27dc6ab8ceaef24691215c197f8d5cd17718b54fbb")
    version("1.1-221", sha256="a6da297a670f756ee964ffd99c3b212c55c297d385583fd0e767435dd5cd4ccd")
    version("1.1-20", sha256="d6a261ce8f487d5d03b1931039f528f2eb50fb9386e7aae40045c966ff6d4182")
    version("1.1-13", sha256="02d94977bfa2f41f1db60e619335ac0ea8109dd98108ff9d21a412f7c4a14a2e")
    version("1.1-12", sha256="6dc4a8a046e7fced190402f39a9bae6f863e08c320f0881367c022b2f220f14b")
    version("1.1-11", sha256="1caf8fa1914ad6921d76e7b22a8c25cfe55892b0d21aef3b2a7b8f5b79b9388b")

    depends_on("r-r-utils", type=("build", "run"))
