# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTeachingdemos(RPackage):
    """Demonstrations for Teaching and Learning.

    Demonstration functions that can be used in a classroom to demonstrate
    statistical concepts, or on your own to better understand the concepts
    or the programming."""

    cran = "TeachingDemos"

    version("2.13", sha256="f80eb952b7d1a0cde3bed8152f9c4e9eceaa3f635209b2af9a11e785e8c0fbcc")
    version("2.12", sha256="3e75405ce1affa406d6df85e06f96381412bc7a2810b25d8c81bfe64c4698644")
    version("2.10", sha256="2ef4c2e36ba13e32f66000e84281a3616584c86b255bca8643ff3fe4f78ed704")

    depends_on("r@2.10:", type=("build", "run"))
