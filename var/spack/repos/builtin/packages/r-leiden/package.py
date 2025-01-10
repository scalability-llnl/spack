# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLeiden(RPackage):
    """R Implementation of Leiden Clustering Algorithm.

    Implements the 'Python leidenalg' module to be called in R. Enables
    clustering using the leiden algorithm for partition a graph into
    communities. See the 'Python' repository for more details:
    <https://github.com/vtraag/leidenalg> Traag et al (2018) From Louvain to
    Leiden: guaranteeing well-connected communities. <arXiv:1810.08473>."""

    cran = "leiden"

    license("GPL-3.0-only OR custom")

    version("0.4.3.1", sha256="a9ecbbcfa2724d8fdd0133af569278e036b25b6e2cbb23d453092cc6b3fc30e2")
    version("0.4.3", sha256="6a464b4b860e621749b3b701bb7ceb07e23c1a36be241c3e13b18105eb980938")
    version("0.4.2", sha256="cace86748c4aa1720508210658ee2f63f7875be5bac215084001fdc59d22e2bd")
    version("0.3.9", sha256="81754276e026a9a8436476365bbadf0f15a403a525a349cb56418da5d8edea0d")
    version("0.3.6", sha256="a7096e38c4010b1f0baf6a7e1139362520b44c0e548b0b79584cb827172822cc")
    version("0.3.1", sha256="17fa1e49667fdd30ef5166506181c8514ae406f68f0878a026ee111bff11f8a5")

    depends_on("r-reticulate", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-igraph@1.2.7:", type=("build", "run"), when="@0.4.2:")
