# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSqldf(RPackage):
    """Manipulate R Data Frames Using SQL.

    The sqldf() function is typically passed a single argument which is an SQL
    select statement where the table names are ordinary R data frame names.
    sqldf() transparently sets up a database, imports the data frames into that
    database, performs the SQL select or other statement and returns the result
    using a heuristic to determine which class to assign to each column of the
    returned data frame. The sqldf() or read.csv.sql() functions can also be
    used to read filtered files into R even if the original files are larger
    than R itself can handle. 'RSQLite', 'RH2', 'RMySQL' and 'RPostgreSQL'
    backends are supported."""

    cran = "sqldf"

    license("GPL-2.0-only")

    version("0.4-11", sha256="cee979d4e8c67b4924655365d925a8d67104e62adf71741f645cdc5196de2260")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-gsubfn@0.6:", type=("build", "run"))
    depends_on("r-proto", type=("build", "run"))
    depends_on("r-rsqlite", type=("build", "run"))
    depends_on("r-dbi", type=("build", "run"))
    depends_on("r-chron", type=("build", "run"))
