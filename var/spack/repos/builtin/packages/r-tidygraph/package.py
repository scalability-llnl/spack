# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidygraph(RPackage):
    """A Tidy API for Graph Manipulation.

    A graph, while not "tidy" in itself, can be thought of as two tidy data
    frames describing node and edge data respectively. 'tidygraph' provides an
    approach to manipulate these two virtual data frames using the API defined
    in the 'dplyr' package, as well as provides tidy interfaces to a lot of
    common graph algorithms."""

    cran = "tidygraph"

    license("MIT")

    version("1.3.1", sha256="aac1d4bb9396081bbeecbde11a3cd1a26a56bd6b1f608a628b359cb37c18ac1a")
    version("1.2.3", sha256="b09c06b12583ae57edd1ec01e61a0e1b7a4b82358361fb28a6046dbece475687")
    version("1.2.2", sha256="d555cad6b5b56bd2edaa29950a0fd15942e972db21561bfd5cd64fd9a8936470")
    version("1.2.1", sha256="2fbdc2db18c5ad48c72f14d2d04111f4b0d4c434ad87c280eda3bcb98673ad36")
    version("1.2.0", sha256="057d6c42fc0144109f3ace7f5058cca7b2fe493c761daa991448b23f86b6129f")
    version("1.1.2", sha256="5642001d4cccb122d66481b7c61a06c724c02007cbd356ee61cb29726a56fafe")

    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-dplyr@0.8:", type=("build", "run"))
    depends_on("r-dplyr@0.8.5:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-igraph@1.3.0:", type=("build", "run"), when="@1.2.3:")
    depends_on("r-igraph@2.0.0:", type=("build", "run"), when="@1.3.1:")
    depends_on("r-lifecycle", type=("build", "run"), when="@1.3.0:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
    depends_on("r-pillar", type=("build", "run"))
    depends_on("r-cli", type=("build", "run"), when="@1.2.1:")
    depends_on("r-cpp11", type=("build", "run"), when="@1.2.1:")

    depends_on("r-rcpp", type=("build", "run"), when="@:1.2.0")
