# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMultcomp(RPackage):
    """Simultaneous Inference in General Parametric Models.

    Simultaneous tests and confidence intervals for general linear hypotheses
    in parametric models, including linear, generalized linear, linear mixed
    effects, and survival models. The package includes demos reproducing
    analyzes presented in the book "Multiple Comparisons Using R" (Bretz,
    Hothorn, Westfall, 2010, CRC Press)."""

    cran = "multcomp"

    license("GPL-2.0-only")

    version("1.4-26", sha256="a100bbdfaffb8b9cf9a59decf80267421673c4f1eef44c0bc3f77be16b3a69ec")
    version("1.4-23", sha256="425154a58bd8f2dbaff5d16e97b03473cbc0d571b1c2e4dd66a13c6d20a8cde1")
    version("1.4-20", sha256="328be4fa4189bde4a7bc645d9ae5ea071ebe31ed658c8c48c4e45aa8e8c42cfc")
    version("1.4-19", sha256="f03473b1cfbc714cd85a0ee948e2ecdb23bcdccbe95e27237ee25e9c71e3e557")
    version("1.4-18", sha256="107a5e65cfff158b271d7386240dc8672d8cf45313f016e0ed83767faf7c2806")
    version("1.4-15", sha256="9927607efb3eb84ac3d25d82daf2faef6a69e05a334b163ce43fd31c14b19bce")
    version("1.4-10", sha256="29bcc635c0262e304551b139cd9ee655ab25a908d9693e1cacabfc2a936df5cf")
    version("1.4-8", sha256="a20876619312310e9523d67e9090af501383ce49dc6113c6b4ca30f9c943a73a")
    version("1.4-6", sha256="fe9efbe671416a49819cbdb9137cc218faebcd76e0f170fd1c8d3c84c42eeda2")

    depends_on("r-mvtnorm@1.0-10:", type=("build", "run"))
    depends_on("r-survival@2.39-4:", type=("build", "run"))
    depends_on("r-th-data@1.0-2:", type=("build", "run"))
    depends_on("r-sandwich@2.3-0:", type=("build", "run"))
    depends_on("r-codetools", type=("build", "run"))
