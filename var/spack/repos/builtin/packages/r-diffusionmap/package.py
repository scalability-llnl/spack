# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDiffusionmap(RPackage):
    """Diffusion Map.

    Implements diffusion map method of data parametrization, including creation
    and visualization of diffusion map, clustering with diffusion K-means and
    regression using adaptive regression model. Richards (2009)
    <doi:10.1088/0004-637X/691/1/32>."""

    cran = "diffusionMap"

    version("1.2.0", sha256="523847592fbc3a29252bc92b5821e17564ce6b188c483c930e95e6950c3873e7")
    version("1.1-0.1", sha256="b24cf841af2566ac36f4ede2885f2ff355a7905398444d6d89747315d99a8486")
    version("1.1-0", sha256="637b810140145fa0cbafb1c13da347c2f456c425334ae554d11a3107052e28d1")
    version("1.0-0", sha256="1e3c54f72cbb2bce1b06b85fda33242b9041d30d4ac8c12df4dc9a3a95a44044")
    version("0.0-2", sha256="b08b9d8a7b2b49d8f809ed14ab40cec92a635a284e43af068eb34e74172c0bcf")
    version("0.0-1", sha256="38c4af2d2a4fa4116c2e01a5e67ba313e7a8e76f724a3312a3c12b26e299f844")

    depends_on("r@2.4.0:", type=("build", "run"))
    depends_on("r@2.10:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-scatterplot3d", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
