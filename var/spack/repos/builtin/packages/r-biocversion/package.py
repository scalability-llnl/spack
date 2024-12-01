# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocversion(RPackage):
    """Set the appropriate version of Bioconductor packages.

    This package provides repository information for the appropriate
    version of Bioconductor."""

    bioc = "BiocVersion"

    version("3.17.1", commit="a2d0c4c489be1cafdb51bf8d205161429b09ac7f")
    version("3.16.0", commit="c681e06fe30ea6815f958c1a3c74c090863680ba")
    version("3.15.2", commit="818ab03b6a3551993b712e3702126040f9fb7600")
    version("3.14.0", commit="aa56d93d0ea5dcdbf301f120502981740fd91e1e")
    version("3.12.0", commit="23b971963c6b73550a7e330dab5a046d58ce0223")

    depends_on("r@4.0.0:", type=("build", "run"))
    depends_on("r@4.1.0:", type=("build", "run"), when="@3.14.0:")
    depends_on("r@4.2.0:", type=("build", "run"), when="@3.15.2:")
    depends_on("r@4.3.0:", type=("build", "run"), when="@3.17.1:")
