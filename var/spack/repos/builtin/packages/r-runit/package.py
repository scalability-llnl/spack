# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRunit(RPackage):
    """R Unit Test Framework.

    R functions implementing a standard Unit Testing framework, with additional
    code inspection and report generation tools."""

    cran = "RUnit"

    license("GPL-2.0-only")

    version("0.4.33", sha256="b2a4c5afc7ef9534dac5006f6ef1b2af68630bb73eb74ef70ec7ed53dae6cb5f")
    version("0.4.32", sha256="23a393059989000734898685d0d5509ece219879713eb09083f7707f167f81f1")

    depends_on("r@2.5.0:", type=("build", "run"))
