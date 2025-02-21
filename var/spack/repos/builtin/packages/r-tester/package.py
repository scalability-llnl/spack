# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTester(RPackage):
    """Tests and checks characteristics of R objects.

    tester allows you to test characteristics of common R objects."""

    cran = "tester"

    license("GPL-3.0-only")

    version("0.2.0", sha256="bec8141b8572ca8d19a270a2eaec23aa4c01a167f32f2e05a4bf353418a0020b")
    version("0.1.7", sha256="b9c645119c21c69450f3d366c911ed92ac7c14ef61652fd676a38fb9d420b5f4")

    depends_on("r@3.0:", type=("build", "run"))
