# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAplot(RPackage):
    """Decorate a 'ggplot' with Associated Information.

    For many times, we are not just aligning plots as what 'cowplot' and
    'patchwork' did. Users would like to align associated information that
    requires axes to be exactly matched in subplots, e.g. hierarchical
    clustering with a heatmap. This package provides utilities to aligns
    associated subplots to a main plot at different sides (left, right, top and
    bottom) with axes exactly matched."""

    cran = "aplot"

    license("Artistic-2.0")

    version("0.2.3", sha256="1fb062050199933f724164118cc3e5d85b60a3a4d4a466016bed2928b0310d6a")
    version("0.1.10", sha256="d937768241f887628b88bb3b49dd6cbe9b7dae39ae7054e7380a9836721a67d1")
    version("0.1.8", sha256="d931d7769dc7ce4bc938e8c068973721e89da0aa5f40a04f8a9119621b33459c")
    version("0.1.7", sha256="f6250f5f6d1addc8d5717be80a92c569bfd83d35bce2e3dbeb251c9ae1be8616")
    version("0.1.6", sha256="7d69d1968bc613d8ceccc05c53362b0f62b632e1c6ef5100c91b65b15afa200c")
    version("0.1.4", sha256="cde9dfc1c6b38e370c1f7338651c37727efa57d52b646fec6b021855809492ac")
    version("0.1.2", sha256="899c4d101ddcedb1eba9803d78cf02288b63de25e2879add8add1165167509f0")

    depends_on("r@4.1.0:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-ggfun@0.0.4:", type=("build", "run"), when="@0.1.2:")
    depends_on("r-ggfun@0.0.6:", type=("build", "run"), when="@0.1.4:")
    depends_on("r-ggfun@0.0.9:", type=("build", "run"), when="@0.1.10:")
    depends_on("r-ggfun@0.1.3:", type=("build", "run"), when="@0.2.1:")
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-ggplotify", type=("build", "run"))
    depends_on("r-patchwork", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))

    depends_on("r-yulab-utils", type=("build", "run"), when="@0.1.2")
