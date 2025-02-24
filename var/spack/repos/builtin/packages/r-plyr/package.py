# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPlyr(RPackage):
    """Tools for Splitting, Applying and Combining Data.

    A set of tools that solves a common set of problems: you need to break a
    big problem down into manageable pieces, operate on each piece and then put
    all the pieces back together. For example, you might want to fit a model to
    each spatial location or time point in your study, summarise data by panels
    or collapse high-dimensional arrays to simpler summary statistics. The
    development of 'plyr' has been generously supported by 'Becton
    Dickinson'."""

    cran = "plyr"

    license("MIT")

    version("1.8.9", sha256="15b5e7f711d53bf41b8687923983b8ef424563aa2f74c5195feb5b1df1aee103")
    version("1.8.8", sha256="a73211b4bbe13e4e5e764966a8dd90172c1cc311938dd464d142e1c7a701070c")
    version("1.8.7", sha256="7d9fdaf1157035a49c3661da3bbaa7bfcf782aafe1b98f7b5a68b0520046e87f")
    version("1.8.6", sha256="ea55d26f155443e9774769531daa5d4c20a0697bb53abd832e891b126c935287")
    version("1.8.4", sha256="60b522d75961007658c9806f8394db27989f1154727cb0bb970062c96ec9eac5")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
