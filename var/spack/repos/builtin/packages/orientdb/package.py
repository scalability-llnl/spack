# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Orientdb(MavenPackage):
    """OrientDB is an Open Source Multi-Model NoSQL DBMS with the support
    of Native Graphs, Documents Full-Text, Reactivity, Geo-Spatial and Object
    Oriented concepts. It's written in Java and it's amazingly fast."""

    homepage = "https://orientdb.org"
    url = "https://github.com/orientechnologies/orientdb/archive/3.1.2.tar.gz"

    license("Apache-2.0")

    version("3.1.2", sha256="3c8e1f55de9e1a6c3cd714832deb7369f50096e85f1e048f0c0328e611970850")
    version("3.1.1", sha256="d5cc6b6048b71696a4a592705c2a3aec65757eca3cfadb03905306ceb4348d37")
    version("3.1.0", sha256="84f7ced66847fc5a7b987c701d60302e2aff63cdac2869941eee158251515b99")
