# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDichromat(RPackage):
    """Color Schemes for Dichromats.

    Collapse red-green or green-blue distinctions to simulate the effects of
    different types of color-blindness."""

    cran = "dichromat"

    license("GPL-2.0-only")

    version("2.0-0.1", sha256="a10578e9ad8a581bd8fe0d8a8370051f3cdcf12c7d282f3af2a18dacda566081")
    version("2.0-0", sha256="31151eaf36f70bdc1172da5ff5088ee51cc0a3db4ead59c7c38c25316d580dd1")

    depends_on("r@2.10:", type=("build", "run"))
