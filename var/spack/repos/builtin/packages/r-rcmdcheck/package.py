# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcmdcheck(RPackage):
    """Run 'R CMD check' from 'R' and Capture Results.

    Run 'R CMD check' from 'R' and capture the results of the individual
    checks. Supports running checks in the background, timeouts, pretty
    printing and comparing check results."""

    cran = "rcmdcheck"

    license("MIT")

    version("1.4.0", sha256="bbd4ef7d514b8c2076196a7c4a6041d34623d55fbe73f2771758ce61fd32c9d0")
    version("1.3.3", sha256="1ab679eb1976d74cd3be5bcad0af7fcc673dbdfd4406bbce32591c8fddfb93b4")

    depends_on("r-callr@3.1.1.9000:", type=("build", "run"))
    depends_on("r-cli@1.1.0:", type=("build", "run"))
    depends_on("r-cli@3.0.0:", type=("build", "run"), when="@1.4.0:")
    depends_on("r-curl", type=("build", "run"), when="@1.4.0:")
    depends_on("r-desc@1.2.0:", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-pkgbuild", type=("build", "run"))
    depends_on("r-prettyunits", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-rprojroot", type=("build", "run"))
    depends_on("r-sessioninfo@1.1.1:", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-xopen", type=("build", "run"))

    depends_on("r-crayon", type=("build", "run"), when="@:1.3.3")
