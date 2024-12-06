# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kylin(MavenPackage):
    """Apache Kylin is an open source, distributed Analytical Data
    Warehouse for Big Data; it was designed to provide OLAP (Online
    Analytical Processing) capability in the big data era. By renovating
    the multi-dimensional cube and precalculation technology on Hadoop
    and Spark, Kylin is able to achieve near constant query speed
    regardless of the ever-growing data volume. Reducing query latency
    from minutes to sub-second, Kylin brings online analytics back to big
    data."""

    homepage = "https://kylin.apache.org"
    url = "https://github.com/apache/kylin/archive/kylin-3.1.0.tar.gz"

    license("Apache-2.0")

    version("3.1.0", sha256="84073ff16a0dad6e0611fea9fbf2b977b6bac307107a222b7f576a3a3b712157")

    depends_on("cxx", type="build")  # generated

    depends_on("java@8", type=("build", "run"))
