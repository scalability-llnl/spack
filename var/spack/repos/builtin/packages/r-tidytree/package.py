# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidytree(RPackage):
    """A Tidy Tool for Phylogenetic Tree Data Manipulation.

    Phylogenetic tree generally contains multiple components including node,
    edge, branch and associated data. 'tidytree' provides an approach to
    convert tree object to tidy data frame as well as provides tidy interfaces
    to manipulate tree data."""

    cran = "tidytree"

    license("Artistic-2.0")

    version("0.4.6", sha256="dba909ba767283fa76795a67e048ff1c8cd339c7e44f64c9698c70ecb3d92292")
    version("0.4.2", sha256="cb831a66d8afa5e21f5072e4fbebcbd2228881090d0040f87605f5aeefda155e")
    version("0.4.1", sha256="fbc4364d17e1b1c26ed06af0cdf36c88a5bc562fdbd4731ab179e30bba4009eb")
    version("0.3.9", sha256="12435d4f4c4d734b2a758cb13eb3b44bdfa8fdfa79a6e81fb99f7ce3a5d82edf")
    version("0.3.7", sha256="7816f2d48ec94ca0c1bef15ec3d536adf44a969ea3c3cfc203ceebe16808e4f2")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-lazyeval", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
    depends_on("r-tidyselect", type=("build", "run"))
    depends_on("r-yulab-utils@0.0.4:", type=("build", "run"))
    depends_on("r-pillar", type=("build", "run"), when="@0.3.9:")
    depends_on("r-cli", type=("build", "run"), when="@0.4.2:")
