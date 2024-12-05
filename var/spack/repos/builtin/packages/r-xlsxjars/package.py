# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXlsxjars(RPackage):
    """Package required POI jars for the xlsx package.

    The xlsxjars package collects all the external jars required for the xlxs
    package. This release corresponds to POI 3.10.1."""

    cran = "xlsxjars"

    license("GPL-3.0-only")

    version("0.6.1", sha256="37c1517f95f8bca6e3514429394d2457b9e62383305eba288416fb53ab2e6ae6")

    depends_on("r-rjava", type=("build", "run"))
