# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFlashclust(RPackage):
    """Implementation of optimal hierarchical clustering."""

    cran = "flashClust"

    version("1.01-2", sha256="48a7849bb86530465ff3fbfac1c273f0df4b846e67d5eee87187d250c8bf9450")

    depends_on("fortran", type="build")  # generated

    depends_on("r@2.3.0:", type=("build", "run"))
