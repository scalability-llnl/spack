# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BioconductorDupradar(RPackage):
    """Assessment of duplication rates in RNA-Seq datasets"""

    homepage = "https://bioconductor.org/packages/3.16/bioc/html/dupRadar.html"
    url = "https://bioconductor.org/packages/release/bioc/src/contrib/dupRadar_1.30.0.tar.gz"
    maintainers("pabloaledo")

    bioc = "dupradar"

    version(
        "1.30.0",
        sha256="a299d7a4578047dfc19237e34255b0f50f70ce41d29762ef9f5a7741ba35aa3d",
        deprecated=True,
    )

    depends_on("r-kernsmooth")
    depends_on("subread")
    depends_on("bioconductor-rsubread")
