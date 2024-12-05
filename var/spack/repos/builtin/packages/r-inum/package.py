# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RInum(RPackage):
    """Interval and Enum-Type Representation of Vectors.

    Enum-type representation of vectors and representation of intervals,
    including a method of coercing variables in data frames."""

    cran = "inum"

    license("GPL-2.0-only")

    version("1.0-5", sha256="e696b7e0b31b3bbf405112e60691b6a72fedcaa02e08ee517c59f6bf9cd36bbd")
    version("1.0-4", sha256="5febef69c43a4b95b376c1418550a949d988a5f26b1383ca01c9728a94fc13ce")
    version("1.0-1", sha256="3c2f94c13c03607e05817e4859595592068b55e810fed94e29bc181ad248a099")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-libcoin@1.0-0:", type=("build", "run"))
