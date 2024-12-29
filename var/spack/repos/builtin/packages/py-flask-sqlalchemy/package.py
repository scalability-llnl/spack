# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskSqlalchemy(PythonPackage):
    """
    Add SQLAlchemy support to your Flask application.
    """

    homepage = "https://github.com/pallets-eco/flask-sqlalchemy"
    pypi = "flask-sqlalchemy/Flask-SQLAlchemy-3.0.2.tar.gz"

    maintainers("charmoniumq")

    license("BSD-3-Clause")

    # If py-slqalchemy@1.4.18: is too restrictive, consider downgrading py-flask-sqlalchemy to @2.
    version("3.0.2", sha256="16199f5b3ddfb69e0df2f52ae4c76aedbfec823462349dabb21a1b2e0a2b65e9")
    version("2.5.1", sha256="2bda44b43e7cacb15d4e05ff3cc1f8bc97936cc464623424102bfc2c35e95912")

    with when("@3"):
        # https://github.com/pallets-eco/flask-sqlalchemy/blob/3.0.2/pyproject.toml
        depends_on("python@3.7:", type=("build", "run"))
        depends_on("py-flask@2.2:", type=("build", "run"))
        depends_on("py-sqlalchemy@1.4.18:", type=("build", "run"))
        depends_on("py-pdm-pep517@1:", type="build")

    with when("@2"):
        # https://github.com/pallets-eco/flask-sqlalchemy/blob/2.5.1/setup.py
        depends_on("py-flask@0.10:", type=("build", "run"))
        depends_on("py-sqlalchemy@0.8.0:", type=("build", "run"))
        depends_on("py-setuptools", type="build")
