# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWritexl(RPackage):
    """Zero-dependency data frame to xlsx exporter based on 'libxlsxwriter'.
    Fast and no Java or Excel required."""

    homepage = "https://docs.ropensci.org/writexl/"
    cran = "writexl"

    license("BSD-2-Clause", checked_by="wdconinc")

    version("1.5.0", sha256="e253dc58f00abf51e9b727ae132e8b301e359fb23df0afc40c3ebec3fb096dce")

    depends_on("zlib-api", type=("build", "run"))
