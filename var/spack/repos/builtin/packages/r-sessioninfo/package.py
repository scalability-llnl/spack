# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSessioninfo(RPackage):
    """R Session Information.

    Query and print information about the current R session. It is similar to
    'utils::sessionInfo()', but includes more information about packages, and
    where they were installed from."""

    cran = "sessioninfo"

    license("GPL-2.0-only")

    version("1.2.2", sha256="f56283857c53ac8691e3747ed48fe03e893d8ff348235bff7364658bcfb0c7cb")
    version("1.1.1", sha256="166b04678448a7decd50f24afabe5e2ad613e3c55b180ef6e8dd7a870a1dae48")

    depends_on("r@2.10:", type=("build", "run"), when="@1.2.2:")
    depends_on("r-cli", type=("build", "run"))
    depends_on("r-cli@3.1.0:", type=("build", "run"), when="@1.2.2:")

    depends_on("r-withr", type=("build", "run"), when="@:1.1.1")
