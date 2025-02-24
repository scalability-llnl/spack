# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBslib(RPackage):
    """Custom 'Bootstrap' 'Sass' Themes for 'shiny' and 'rmarkdown'.

    Simplifies custom 'CSS' styling of both 'shiny' and 'rmarkdown' via
    'Bootstrap' 'Sass'. Supports both 'Bootstrap' 3 and 4 as well as their
    various 'Bootswatch' themes. An interactive widget is also provided for
    previewing themes in real time."""

    cran = "bslib"

    license("MIT")

    version("0.8.0", sha256="fd182ddb1b128691d2b0c12882361732a23d451dbf4052ba70b11257e8d44b03")
    version("0.4.2", sha256="9a40b7a1bbe409af273e1e940d921ab198ea576548f06f055f552f70ff822f19")
    version("0.4.1", sha256="4ebd1fc84cd19b414e8f8c13fb95270fc28ede125b6e58b08c574ca8c9e0e62f")
    version("0.4.0", sha256="fbea4ecec726f23618e825624f1d9c03939f765ca5a490b171ebf95b815475c2")
    version("0.3.1", sha256="5f5cb56e5cab9039a24cd9d70d73b69c2cab5b2f5f37afc15f71dae0339d9849")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-fastmap@1.1.1:", type=("build", "run"), when="@0.7.0:")
    depends_on("r-htmltools@0.5.2:", type=("build", "run"))
    depends_on("r-htmltools@0.5.4:", type=("build", "run"), when="@0.4.2:")
    depends_on("r-htmltools@0.5.7:", type=("build", "run"), when="@0.6.0:")
    depends_on("r-htmltools@0.5.8:", type=("build", "run"), when="@0.7.0:")
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-sass@0.4.0:", type=("build", "run"))
    depends_on("r-jquerylib@0.1.3:", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@0.6.0:")
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-memoise", type=("build", "run"), when="@0.4.0:")
    depends_on("r-memoise@2.0.1:", type=("build", "run"), when="@0.4.1:")
    depends_on("r-mime", type=("build", "run"), when="@0.4.2:")
    depends_on("r-sass@0.4.0:", type=("build", "run"), when="@0.5.0:")
    depends_on("r-sass@0.4.9:", type=("build", "run"), when="@0.6.2:")
    depends_on("r-base64enc", type=("build", "run"), when="@0.4.2:")
    depends_on("r-cachem", type=("build", "run"), when="@0.4.0:")
