# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRvcheck(RPackage):
    """R/Package Version Check.

    Check latest release version of R and R package (both in 'CRAN',
    'Bioconductor' or 'Github')."""

    cran = "rvcheck"

    license("Artistic-2.0")

    version("0.2.1", sha256="2ad9efd2af8d103e88bff0a01692f0e32515805f269152f2694eadbfe9947026")
    version("0.1.8", sha256="4ca5aa48fbf543e6171696ca7e1bff81e3112d06c919e88769b5c38a115b4718")
    version("0.1.3", sha256="0b59986c1ccc5b89f8aca8fa7cf62d0b875719addb40e08dbda1791cfd334fc4")
    version("0.0.9", sha256="6e7be7b029d28181a1b57ebd4d25978f3459722ffdb45a3698157a7f943bea92")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@0.1.3:")
    depends_on("r-biocmanager", type=("build", "run"), when="@0.1.8:")
    depends_on("r-yulab-utils", type=("build", "run"), when="@0.2.1:")

    depends_on("r-rlang", type=("build", "run"), when="@0.1.1:0.1.8")
