# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFontawesome(RPackage):
    """Easily Work with 'Font Awesome' Icons.

    Easily and flexibly insert 'Font Awesome' icons into 'R Markdown' documents
    and 'Shiny' apps. These icons can be inserted into HTML content through
    inline 'SVG' tags or 'i' tags. There is also a utility function for
    exporting 'Font Awesome' icons as 'PNG' images for those situations where
    raster graphics are needed."""

    cran = "fontawesome"

    license("MIT")

    version("0.5.2", sha256="da3de2a9717084d1400d48edd783f06c66b8c910ce9c8d753d1b7d99be1c5cc9")
    version("0.5.1", sha256="f4ebbbe2ee8d2e2c0342b72095cfe668bd9800ea6c4bf7180300544bde7e566c")
    version("0.4.0", sha256="760a0bc5b50ddbce1160b123f3b3d76342167519d75641dc2c5b952fa8d4242f")
    version("0.3.0", sha256="4deefcf4d4580d84213f863351c2a23c39adbd2f8762d7477ec2faa8235a1a31")
    version("0.2.2", sha256="572db64d1b3c9be301935e0ca7baec69f3a6e0aa802e23f1f224b3724259df64")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-rlang@0.4.10:", type=("build", "run"))
    depends_on("r-rlang@1.0.6:", type=("build", "run"), when="@0.5.1:")
    depends_on("r-htmltools@0.5.1.1:", type=("build", "run"))
