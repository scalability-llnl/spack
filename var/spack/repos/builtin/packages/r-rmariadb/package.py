# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmariadb(RPackage):
    """Database Interface and 'MariaDB' Driver.

    Implements a 'DBI'-compliant interface to 'MariaDB'
    (<https://mariadb.org/>) and 'MySQL' (<https://www.mysql.com/>)
    databases."""

    cran = "RMariaDB"

    version("1.3.2", sha256="7c87ef0623218b9e79dd6a9b1a25f495520289603ca48f54ea45309bd8826828")
    version("1.2.2", sha256="c97c61ace584f9ad9929d3e3f366556e0eecad12bc98ea2979563a01475f468e")
    version("1.2.1", sha256="c9176a096854ce33a98ce0faef0065c50b5d356174f90cea742c70e130cf5f0c")
    version("1.1.0", sha256="9ffa63a15052876a51a7996ca4e6a5b7b937f594b5cc7ca5a86f43789e22a956")
    version("1.0.8", sha256="3c8aedc519dc063ceb068535a3700bc5caf26f867078cc5a228aa8961e2d99f5")

    depends_on("r@2.8.0:", type=("build", "run"))
    depends_on("r-bit64", type=("build", "run"))
    depends_on("r-blob", type=("build", "run"), when="@1.2.1:")
    depends_on("r-dbi@1.1.0:", type=("build", "run"))
    depends_on("r-dbi@1.1.3:", type=("build", "run"), when="@1.2.2:")
    depends_on("r-hms@0.5.0:", type=("build", "run"))
    depends_on("r-lubridate", type=("build", "run"), when="@1.1.0:")
    depends_on("r-cpp11", type=("build", "run"), when="@1.3.0:")
    depends_on("r-rlang", type=("build", "run"), when="@1.2.1:")
    depends_on("r-plogr", type=("build", "run"))
    depends_on("mariadb-client")

    depends_on("r-rcpp@0.12.4:", type=("build", "run"), when="@:1.2.2")
    depends_on("r-bh", type=("build", "run"), when="@:1.1.0")

    # Set the library explicitly to prevent configure from finding a system
    # mysql-client
    def configure_vars(self):
        lib_dir = self.spec["mariadb-client"].prefix.lib.mariadb
        inc_dir = self.spec["mariadb-client"].prefix.include.mariadb
        args = ["LIB_DIR={0}".format(lib_dir), "INCLUDE_DIR={0}".format(inc_dir)]
        return args
