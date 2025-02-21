# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmysql(RPackage):
    """Database Interface and 'MySQL' Driver for R.

    Legacy 'DBI' interface to 'MySQL' / 'MariaDB' based on old code ported from
    S-PLUS. A modern 'MySQL' client based on 'Rcpp' is available  from the
    'RMariaDB' package."""

    cran = "RMySQL"

    version("0.10.27", sha256="f1735b689cd9bdb9c776a16138eaa1f6c5cbdbab5c1d292e1240e3bbf105bfab")
    version("0.10.25", sha256="ed130f9bd80ea9fd5b4fdbb6fa094c35646354507de68eb3d19a3cbc8b5a4794")
    version("0.10.24", sha256="ca1b9aacab6d76866ba09210ae881c3a7555bd5144ea0a0a446fceff80637241")
    version("0.10.23", sha256="f4ac7ed4fba83749819c07ce32d53ee024cf1cedebbda3b832644bff9edf4a15")
    version("0.10.21", sha256="3a6bf06d32d66c7c958d4f89ed517614171a7fd254ef6f4d40f4c5982c2d6b31")
    version("0.10.17", sha256="754df4fce159078c1682ef34fc96aa5ae30981dc91f4f2bada8d1018537255f5")
    version("0.10.9", sha256="41289c743dc8ee2e0dea8b8f291d65f0a7cd11e799b713d94840406ff296fd42")

    depends_on("r@2.8.0:", type=("build", "run"))
    depends_on("r-dbi@0.4:", type=("build", "run"))
    depends_on("mariadb-client")
