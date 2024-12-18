# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMysqldb1(PythonPackage):
    """Legacy mysql bindings for python"""

    homepage = "https://github.com/farcepest/MySQLdb1"
    url = "https://github.com/farcepest/MySQLdb1/archive/MySQLdb-1.2.5.tar.gz"

    version(
        "1.2.5",
        sha256="905dd8be887ff596641ace5411fed17cfd08dd33699ea627d3fb44f8a922c2f0",
        url="https://github.com/farcepest/MySQLdb1/archive/MySQLdb-1.2.5.tar.gz",
    )

    depends_on("c", type="build")  # generated

    depends_on("mysql@:6")
    depends_on("py-setuptools", type="build")
