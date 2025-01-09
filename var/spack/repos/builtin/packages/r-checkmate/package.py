# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCheckmate(RPackage):
    """Fast and Versatile Argument Checks.

    Tests and assertions to perform frequent argument checks.  A substantial
    part of the package was written in C to minimize any worries about
    execution time overhead."""

    cran = "checkmate"

    license("BSD-3-Clause")

    version("2.3.2", sha256="7255732d6c2da51204128a910e8c0d05246324a0402fca4d0d99433af40a88e3")
    version("2.1.0", sha256="b784dd5163a0350d084ef34882d9781373839dedeaa9a8b8e6187d773d0d21c6")
    version("2.0.0", sha256="0dc25b0e20c04836359df1885d099c6e4ad8ae0e585a9e4107f7ea945d9c6fa4")
    version("1.9.4", sha256="faa25754b757fe483b876f5d07b73f76f69a1baa971420892fadec4af4bbad21")
    version("1.8.4", sha256="6f948883e5a885a1c409d997f0c782e754a549227ec3c8eb18318deceb38f8f6")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-backports@1.1.0:", type=("build", "run"))
