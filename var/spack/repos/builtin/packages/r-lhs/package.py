# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLhs(RPackage):
    """Latin Hypercube Samples.

    Provides a number of methods for creating and augmenting Latin Hypercube
    Samples."""

    cran = "lhs"

    license("GPL-3.0-only")

    version("1.2.0", sha256="6b4b773c6b322f1ffb3e2ef49c244ec8a3958a0346a1cc8f42f0d0951e8b0724")
    version("1.1.6", sha256="e37fce44efe6a371677ba2f72f9e1e48270a0fdc60872d05def89270586cd23f")
    version("1.1.5", sha256="7a3c6fdcc953490e51026e17a0b1a9dc0ca8d03e6fc989457a7cdda2075b6339")
    version("1.1.3", sha256="e43b8d48db1cf26013697e2a798ed1d31d1ee1790f2ebfecb280176c0e0c06d1")
    version("1.1.1", sha256="903e9f2adde87f6f9ad41dd52ff83d28a645dba69934c7535142cb48f10090dc")
    version("1.0.1", sha256="a4d5ac0c6f585f2880364c867fa94e6554698beb65d3678ba5938dd84fc6ea53")
    version("1.0", sha256="38c53482b360bdea89ddcfadf6d45476c80b99aee8902f97c5e97975903e2745")
    version("0.16", sha256="9cd199c3b5b2be1736d585ef0fd39a00e31fc015a053333a7a319668d0809425")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.0:")
    depends_on("r-rcpp", type=("build", "run"), when="@1.0:")
