# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RConflicted(RPackage):
    """An Alternative Conflict Resolution Strategy.

    R's default conflict management system gives the most recently loaded
    package precedence. This can make it hard to detect conflicts, particularly
    when they arise because a package update creates ambiguity that did not
    previously exist. 'conflicted' takes a different approach, making every
    conflict an error and forcing you to choose which function to use."""

    cran = "conflicted"

    license("MIT")

    version("1.2.0", sha256="c99b86bb52da3e7d1f4d96d70c77304d0434db5bd906edd8d743e89ac9223088")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r-cli@3.4.0:", type=("build", "run"))
    depends_on("r-memoise", type=("build", "run"))
    depends_on("r-rlang@1.0.0:", type=("build", "run"))
