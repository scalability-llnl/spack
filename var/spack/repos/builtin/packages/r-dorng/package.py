# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDorng(RPackage):
    """Generic Reproducible Parallel Backend for 'foreach' Loops.

    Provides functions to perform reproducible parallel foreach loops, using
    independent random streams as generated by L'Ecuyer's combined
    multiple-recursive generator (L'Ecuyer (1999),
    <doi:10.1287/opre.47.1.159>).  It enables to easily convert standard
    %dopar% loops into fully reproducible loops, independently of the number of
    workers, the task scheduling strategy, or the chosen parallel environment
    and associated foreach backend."""

    cran = "doRNG"

    version("1.8.6", sha256="5032ade083f1f9841ac2e8d4426faa07f189c25c0c338fa155c5dadbe5507de2")
    version("1.8.2", sha256="33e9d45b91b0fde2e35e911b9758d0c376049121a98a1e4c73a1edfcff11cec9")
    version("1.7.1", sha256="27533d54464889d1c21301594137fc0f536574e3a413d61d7df9463ab12a67e9")
    version("1.6.6", sha256="939c2282c72c0b89fc7510f4bff901a4e99007dc006f46762c8f594c0ecbd876")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-rngtools@1.3:", type=("build", "run"))
    depends_on("r-rngtools@1.5:", type=("build", "run"), when="@1.8.2:")
    depends_on("r-iterators", type=("build", "run"))

    depends_on("r-pkgmaker@0.20:", type=("build", "run"), when="@:1.7.1")
