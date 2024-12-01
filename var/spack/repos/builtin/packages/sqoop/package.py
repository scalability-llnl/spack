# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sqoop(MavenPackage):
    """Apache Sqoop is a tool designed for efficiently transferring bulk
    data between Apache Hadoop and structured datastores such as relational
    databases."""

    homepage = "https://sqoop.apache.org/"
    url = "https://downloads.apache.org/sqoop/1.99.7/sqoop-1.99.7.tar.gz"
    list_url = "https://downloads.apache.org/sqoop/"
    list_depth = 1

    license("Apache-2.0")

    version("1.99.7", sha256="caca533554235d9e999435be59a13b5ecae514b3c914ca3b54868fca43a3b74a")

    depends_on("java@8", type=("build", "run"))
