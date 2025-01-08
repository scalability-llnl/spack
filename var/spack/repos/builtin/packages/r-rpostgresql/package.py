# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRpostgresql(RPackage):
    """R Interface to the 'PostgreSQL' Database System.

    Database interface and PostgreSQL driver for R This package provides a
    Database Interface (DBI) compliant driver for R to access PostgreSQL
    database systems. In order to build and install this package from source,
    PostgreSQL itself must be present your system to provide PostgreSQL
    functionality via its libraries and header files. These files are provided
    as postgresql-devel package under some Linux distributions. On Microsoft
    Windows system the attached libpq library source will be used. A wiki and
    issue tracking system for the package are available at Google Code at
    https://code.google.com/p/rpostgresql/."""

    cran = "RPostgreSQL"

    license("PostgreSQL")

    version("0.7-6", sha256="385939708b6a3657663409f91e165ded0ff5268d1dc6225e0f9b34764baf2d2c")
    version("0.7-5", sha256="6b5401ee55bd948ae7bc84520d789ceb422533a7d5e5bd6e10e3b54447f29fa1")
    version("0.7-4", sha256="b6adf60094f2b03dff1959147cde7f61c2f4c4576d77b2a263c63f8e3cd556c6")
    version("0.7-3", sha256="bdbca10329aeb357f05364772964716dfb5ce2470f7eb4a33770862b6ded71b9")
    version("0.6-2", sha256="080118647208bfa2621bcaac0d324891cc513e07618fa22e3c50ec2050e1b0d5")
    version("0.4-1", sha256="6292e37fa841670a3fb1a0950ceb83d15beb4631c3c532c8ce279d1c0d10bf79")

    depends_on("r@2.9.0:", type=("build", "run"))
    depends_on("r-dbi@0.3:", type=("build", "run"))
    depends_on("postgresql")
