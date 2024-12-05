# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyMariadb(PythonPackage):
    """A module for connecting to mariaDB databases"""

    homepage = "https://github.com/mariadb-corporation/mariadb-connector-python"
    pypi = "mariadb/mariadb-1.1.5.post3.tar.gz"

    license("LGPL-2.1")

    version(
        "1.1.5.post3", sha256="f9336dd4cb3207e621933bb5221f33fac0d7184db64dc44c70531430f4ecdcee"
    )
    version(
        "1.0.10",
        sha256="79028ba6051173dad1ad0be7518389cab70239f92b4ff8b8813dae55c3f2c53d",
        url="https://www.pypi.org/packages/source/m/mariadb/mariadb-1.0.10.zip",
    )

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type=("build", "run"))
    depends_on("mariadb-c-client", type=("build", "run"))
