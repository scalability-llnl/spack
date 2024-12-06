# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPgzip(PythonPackage):
    """A multi-threading implementation of Python gzip module"""

    homepage = "https://github.com/pgzip/pgzip"
    pypi = "pgzip/pgzip-0.3.4.tar.gz"

    license("MIT")

    version("0.3.4", sha256="ef56449039bc6e88558e46fe6bb11e3faaeef445d3985a9fb286795ff842c480")
    version("0.3.1", sha256="a9c2df369311473ec3c239f26bf01638bdc6b6094d89ff4c81c6ef5c84eb24b7")

    depends_on("py-setuptools", type="build")
