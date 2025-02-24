# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFastdummies(RPackage):
    """Fast Creation of Dummy (Binary) Columns and Rows from Categorical
    Variables."""

    homepage = "https://jacobkap.github.io/fastDummies/"
    cran = "fastDummies"

    license("MIT", checked_by="wdconinc")

    version("1.7.4", sha256="95904d4b67efc3faafa47cae9473c9d75653bc3fb6ad0083869ebf9f7960dd08")

    depends_on("r@2.1:", type=("build", "run"))
    depends_on("r@2.10:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
