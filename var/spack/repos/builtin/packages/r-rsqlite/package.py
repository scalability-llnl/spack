# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRsqlite(RPackage):
    """'SQLite' Interface for R.

    This package embeds the SQLite database engine in R and provides an
    interface compliant with the DBI package. The source for the SQLite engine
    (version 3.8.6) is included."""

    cran = "RSQLite"

    version("2.3.7", sha256="25e0572589e64264fe4e5d0495f5d85d977bacbb93a3fc631ede5b078db294ce")
    version("2.3.1", sha256="9ed23e160c401c14e41c40e9930f72697172b2c72933c2d2725a05e81e1f34ca")
    version("2.2.18", sha256="62196adb62ad8ec73ddce573e5391686e9359566e365b123ac4f299809944bea")
    version("2.2.14", sha256="2ae36a875ebc02497985b2ad9ddc6a5434f576e2ab25769580749d9e4f3b607c")
    version("2.2.10", sha256="06aeff33902082ef1ebd5378cd0927df7922aaf377c78acfdd8f34f2888800a8")
    version("2.2.9", sha256="4423f1fea179ecd1c09b0b52bfb684983a27de82d5807590b5fc723697d5bb1c")
    version("2.2.2", sha256="299ceafd4986f60dbca2d705112aa3c29ff68fcbc188d9caaa0493e63a57a873")
    version("2.1.2", sha256="66dad425d22b09651c510bf84b7fc36375ce537782f02585cf1c6856ae82d9c6")
    version("2.1.0", sha256="ad6081be2885be5921b1a44b1896e6a8568c8cff40789f43bfaac9f818767642")
    version("2.0", sha256="7f0fe629f34641c6af1e8a34412f3089ee2d184853843209d97ffe29430ceff6")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-bit64", type=("build", "run"))
    depends_on("r-blob@1.2.0:", type=("build", "run"))
    depends_on("r-dbi@1.0.0:", type=("build", "run"))
    depends_on("r-dbi@1.1.0:", type=("build", "run"), when="@2.2.10:")
    depends_on("r-dbi@1.2.0:", type=("build", "run"), when="@2.3.5:")
    depends_on("r-rlang", type=("build", "run"), when="@2.3.4:")
    depends_on("r-memoise", type=("build", "run"))
    depends_on("r-pkgconfig", type=("build", "run"))
    depends_on("r-plogr@0.2.0:", type=("build", "run"))
    depends_on("r-cpp11@0.4.0:", type=("build", "run"), when="@2.3.1:")

    depends_on("r-bh", type=("build", "run"), when="@:2.2.2")
    depends_on("r-rcpp@0.12.7:", type=("build", "run"), when="@:2.2.18")
    depends_on("r-rcpp@1.0.7:", type=("build", "run"), when="@2.2.9:2.2.18")
