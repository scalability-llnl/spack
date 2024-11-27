# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeobolt(PythonPackage):
    """Neo4j Bolt connector for Python"""

    homepage = "https://github.com/neo4j-drivers/neobolt"
    pypi = "neobolt/neobolt-1.7.16.tar.gz"

    version("1.7.16", sha256="ca4e87679fe3ed39aec23638658e02dbdc6bbc3289a04e826f332e05ab32275d")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
