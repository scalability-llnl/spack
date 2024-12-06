# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BioconductorRsubread(RPackage):
    """Mapping, quantification and variant analysis of sequencing data"""

    homepage = "https://bioconductor.org/packages/3.16/bioc/html/Rsubread.html"
    url = "https://bioconductor.org/packages/release/bioc/src/contrib/Rsubread_2.14.2.tar.gz"

    bioc = "rsubread"

    depends_on("r-matrix")
    depends_on("zlib-api")

    version(
        "2.14.2",
        sha256="ac8be0fad0eb2743443e3a60a9a94eec78c746638aaccca70e7166d034dcebb5",
        deprecated=True,
    )
