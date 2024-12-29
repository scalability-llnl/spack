# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Neo4j(MavenPackage):
    """Neo4j is the world's leading Graph Database. It is a high performance
    graph store with all the features expected of a mature and robust
    database, like a friendly query language and ACID transactions. The
    programmer works with a flexible network structure of nodes and
    relationships rather than static tables--yet enjoys all the benefits of
    enterprise-quality database. For many applications, Neo4j offers orders
    of magnitude performance benefits compared to relational DBs."""

    homepage = "https://neo4j.com/"
    url = "https://github.com/neo4j/neo4j/archive/5.17.0.tar.gz"

    license("GPL-3.0-or-later")

    version("5.17.0", sha256="13f43f099978ac639fd9008decaa783f04e3bd3d6957dd5109539e894dad879b")
    version("4.0.3", sha256="19d79052657665dd661bbe906b3552b88108bf379d39fa007b883fff718cabee")
    version("4.0.1", sha256="3f91f566e49000119c6a71d6127e73cfccdee37b68133a067b2ee05932c26dba")
    version("4.0.0", sha256="7173b97baf53be82b46f95fa52f99af591606a318e03915917ddd7141936fec5")
    version("3.5.16", sha256="1304fcd56b0f08f35b05d8b546fd844637ba1ffa5e00bb1e9a81a06b6242cb88")

    depends_on("maven@3.8.2:", type="build", when="@5:")
    depends_on("maven@3.6.2:", type="build", when="@4.4:")
    depends_on("maven@3.5.4:", type="build")
