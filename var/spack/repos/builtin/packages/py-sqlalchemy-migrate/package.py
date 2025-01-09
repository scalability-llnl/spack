# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySqlalchemyMigrate(PythonPackage):
    """Database schema migration for SQLAlchemy"""

    homepage = "https://www.openstack.org/"
    pypi = "sqlalchemy-migrate/sqlalchemy-migrate-0.13.0.tar.gz"

    license("MIT")

    version("0.13.0", sha256="0bc02e292a040ade5e35a01d3ea744119e1309cdddb704fdb99bac13236614f8")

    depends_on("py-setuptools", type="build")
    depends_on("py-pbr@1.8:", type="build")

    depends_on("py-sqlalchemy@0.9.6:", type=("build", "run"))
    depends_on("py-decorator", type=("build", "run"))
    depends_on("py-six@1.7.0:", type=("build", "run"))
    depends_on("py-sqlparse", type=("build", "run"))
    depends_on("py-tempita@0.4:", type=("build", "run"))
