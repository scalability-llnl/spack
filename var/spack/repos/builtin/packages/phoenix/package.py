# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Phoenix(MavenPackage):
    """Apache Phoenix is a SQL skin over HBase delivered as a client-embedded
    JDBC driver targeting low latency queries over HBase data."""

    homepage = "https://github.com"
    git = "https://github.com/apache/phoenix.git"

    license("Apache-2.0")

    version("master", branch="master")
