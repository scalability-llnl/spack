# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RPryr(RPackage):
    """Tools for Computing on the Language.

    Useful tools to pry back the covers of R and understand the language at a
    deeper level."""

    cran = "pryr"

    license("GPL-2.0-only")

    version("0.1.6", sha256="68c1a30a42808eb01a64d31e521d21f2fd5a88dd2c14d05b4b7986d27a177704")
    version("0.1.5", sha256="7b1653ec51850f4633cee8e2eb7d0b2724fb587b801539488b426cf88f0f770b")
    version("0.1.4", sha256="d39834316504c49ecd4936cbbcaf3ee3dae6ded287af42475bf38c9e682f721b")
    version("0.1.3", sha256="6acd88341dde4fe247a5cafd3949b281dc6742b7d60f68b57c1feb84b96739ac")
    version("0.1.2", sha256="65c2b7c9f96e2aa683ac9cdab3c215fd3039ecd66a2ba7002a8e77881428c3c6")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-codetools", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-lobstr", type=("build", "run"), when="@0.1.5:")
