# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPool(RPackage):
    """Object Pooling.

    Enables the creation of object pools, which make it less computationally
    expensive to fetch a new object. Currently the only supported pooled
    objects are 'DBI' connections."""

    cran = "pool"

    license("MIT")

    version("1.0.3", sha256="c461f96928c3e524a52018160d2406f3a1f5ef5abbae54ae89fe7ecd4c1a1cec")
    version("1.0.1", sha256="73d5dffd55e80fdadb88401f12570fcf08e932c4c86761931241f9841fddadbf")
    version("0.1.6", sha256="cdbe5f6c7f757c01893dc9870df0fb8d300829da0e427f6c2559b01caa52d9e1")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.0.2:")
    depends_on("r-dbi", type=("build", "run"))
    depends_on("r-dbi@1.2.1:", type=("build", "run"), when="@1.0.3:")
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-later@1.0.0:", type=("build", "run"))

    depends_on("r-withr", type=("build", "run"), when="@1.0.1")
