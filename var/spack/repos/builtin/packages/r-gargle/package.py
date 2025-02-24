# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGargle(RPackage):
    """Utilities for Working with Google APIs.

    Provides utilities for working with Google APIs
    <https://developers.google.com/apis-explorer>. This includes functions and
    classes for handling common credential types and for preparing, executing,
    and processing HTTP requests."""

    cran = "gargle"

    license("MIT")

    version("1.5.2", sha256="4a5beb046eb50a168b4baf5d1fcd8ac20d698e7fcb6b6ef46a436ded5b039001")
    version("1.4.0", sha256="8e0f1edf5595d4fd27bd92f98af1cc0c1349975803d9d6f3ff0c25ee2440498b")
    version("1.2.1", sha256="f367e2c82f403167ae84058303a4fb0402664558a2abf0b495474a7ef1a2f020")
    version("1.2.0", sha256="4d46ca2933f19429ca5a2cfe47b4130a75c7cd9931c7758ade55bac0c091d73b")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@1.2.1:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-cli@3.0.0:", type=("build", "run"))
    depends_on("r-cli@3.0.1:", type=("build", "run"), when="@1.4.0:")
    depends_on("r-fs@1.3.1:", type=("build", "run"))
    depends_on("r-glue@1.3.0:", type=("build", "run"))
    depends_on("r-httr@1.4.0:", type=("build", "run"))
    depends_on("r-httr@1.4.5:", type=("build", "run"), when="@1.4.0:")
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-openssl", type=("build", "run"), when="@1.4.0:")
    depends_on("r-lifecycle", type=("build", "run"), when="@1.4.0:")
    depends_on("r-rappdirs", type=("build", "run"))
    depends_on("r-rlang@0.4.9:", type=("build", "run"))
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@1.2.1:")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@1.4.0:")
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-rstudioapi", type=("build", "run"), when="@:1.2.1")
