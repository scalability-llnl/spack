# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRio(RPackage):
    """A Swiss-Army Knife for Data I/O.

    Streamlined data import and export by making assumptions that the user
    is probably willing to make: 'import()' and 'export()' determine the data
    structure from the file extension, reasonable defaults are used for data
    import and export (e.g., 'stringsAsFactors=FALSE'), web-based import is
    natively supported (including from SSL/HTTPS), compressed files can be read
    directly without explicit decompression, and fast import packages are used
    where appropriate. An additional convenience function, 'convert()',
    provides a simple method for converting between file types."""

    cran = "rio"

    license("GPL-2.0-only")

    version("1.2.2", sha256="51472a286ad82e1cafd4d87d774662650ccf40d788b59dc70e49fe754e045394")
    version("0.5.29", sha256="9fa63187e1814053e6ed2a164665b4924e08c3453adccb78f7211d403dcc5412")
    version("0.5.16", sha256="d3eb8d5a11e0a3d26169bb9d08f834a51a6516a349854250629072d59c29d465")

    depends_on("r@2.15.0:", type=("build", "run"))
    depends_on("r@4.0:", when="@1.2:", type=("build", "run"))
    depends_on("r-foreign", type=("build", "run"))
    depends_on("r-haven@1.1.2:", type=("build", "run"), when="@0.5.26:")
    depends_on("r-haven@1.1.0:", type=("build", "run"))
    depends_on("r-curl@0.6:", type=("build", "run"))
    depends_on("r-data-table@1.11.2:", when="@1:", type=("build", "run"))
    depends_on("r-data-table@1.9.8:", type=("build", "run"))
    depends_on("r-lifecycle", when="@1:", type=("build", "run"))
    depends_on("r-r-utils", when="@1:", type=("build", "run"))
    depends_on("r-readr", when="@1.2.1:", type=("build", "run"))
    depends_on("r-readxl@0.1.1:", type=("build", "run"))
    depends_on("r-openxlsx", type=("build", "run"), when="@:0.5.30")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-writexl", when="@1:", type=("build", "run"))
