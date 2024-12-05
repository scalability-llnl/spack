# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySqlalchemyUtils(PythonPackage):
    """Various utility functions and custom data types for SQLAlchemy."""

    homepage = "https://github.com/kvesteri/sqlalchemy-utils"
    pypi = "sqlalchemy-utils/SQLAlchemy-Utils-0.36.8.tar.gz"

    license("BSD-3-Clause")

    version("0.41.1", sha256="a2181bff01eeb84479e38571d2c0718eb52042f9afd8c194d0d02877e84b7d74")
    version("0.36.8", sha256="fb66e9956e41340011b70b80f898fde6064ec1817af77199ee21ace71d7d6ab0")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"), when="@0.36.8")
    depends_on("py-sqlalchemy@1.0:", type=("build", "run"), when="@0.36.8")
    depends_on("py-sqlalchemy@1.3:", type=("build", "run"), when="@0.41.1")
    depends_on("py-importlib-metadata", type=("build", "run"), when="@0.41.1 ^python@:3.7")
