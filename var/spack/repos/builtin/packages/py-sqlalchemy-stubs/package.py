# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySqlalchemyStubs(PythonPackage):
    """
    Mypy plugin and stubs for SQLAlchemy
    """

    homepage = "https://github.com/dropbox/sqlalchemy-stubs"
    pypi = "sqlalchemy-stubs/sqlalchemy-stubs-0.4.tar.gz"

    version("0.4", sha256="c665d6dd4482ef642f01027fa06c3d5e91befabb219dc71fc2a09e7d7695f7ae")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-mypy@0.790:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
