# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXtable(RPackage):
    """Export Tables to LaTeX or HTML.

    Coerce data to LaTeX and HTML tables."""

    cran = "xtable"

    license("GPL-2.0-or-later")

    version("1.8-4", sha256="5abec0e8c27865ef0880f1d19c9f9ca7cc0fd24eadaa72bcd270c3fb4075fd1c")
    version("1.8-3", sha256="53b2b0fff8d7a8bba434063c2a01b867f510a4389ded2691fbedbc845f08c325")
    version("1.8-2", sha256="1623a1cde2e130fedb46f98840c3a882f1cbb167b292ef2bd86d70baefc4280d")

    depends_on("r@2.10.0:", type=("build", "run"))
