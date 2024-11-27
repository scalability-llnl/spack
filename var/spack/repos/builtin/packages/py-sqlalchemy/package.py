# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySqlalchemy(PythonPackage):
    """The Python SQL Toolkit and Object Relational Mapper"""

    homepage = "http://www.sqlalchemy.org/"
    pypi = "SQLAlchemy/SQLAlchemy-1.3.9.tar.gz"
    git = "https://github.com/sqlalchemy/sqlalchemy.git"

    license("MIT")

    version("2.0.19", sha256="77a14fa20264af73ddcdb1e2b9c5a829b8cc6b8304d0f093271980e36c200a3f")
    version("1.4.49", sha256="06ff25cbae30c396c4b7737464f2a7fc37a67b7da409993b182b024cec80aed9")
    version("1.4.45", sha256="fd69850860093a3f69fefe0ab56d041edfdfe18510b53d9a2eaecba2f15fa795")
    version("1.4.44", sha256="2dda5f96719ae89b3ec0f1b79698d86eb9aecb1d54e990abb3fdd92c04b46a90")
    version("1.4.25", sha256="1adf3d25e2e33afbcd48cfad8076f9378793be43e7fec3e4334306cac6bec138")
    version("1.4.20", sha256="38ee3a266afef2978e82824650457f70c5d74ec0cadec1b10fe5ed6f038eb5d0")
    version("1.3.19", sha256="3bba2e9fbedb0511769780fe1d63007081008c5c2d7d715e91858c94dbaa260e")
    version("1.3.9", sha256="272a835758908412e75e87f75dd0179a51422715c125ce42109632910526b1fd")
    version("1.2.19", sha256="5bb2c4fc2bcc3447ad45716c66581eab982c007dcf925482498d8733f86f17c7")
    version("1.2.10", sha256="72325e67fb85f6e9ad304c603d83626d1df684fdf0c7ab1f0352e71feeab69d8")
    version("1.1.18", sha256="8b0ec71af9291191ba83a91c03d157b19ab3e7119e27da97932a4773a3f664a9")
    version("1.0.12", sha256="6679e20eae780b67ba136a4a76f83bb264debaac2542beefe02069d0206518d1")

    variant(
        "backend",
        description="Python modules for database access",
        values=any_combination_of("mysql", "postgresql", "pymysql"),
    )

    depends_on("py-setuptools@47:", when="@2:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.24:", when="@2:", type="build")

    depends_on("py-importlib-metadata", when="@1.4.0: ^python@:3.7", type=("build", "run"))
    depends_on("py-greenlet", when="@1.4.0:", type=("build", "run"))
    conflicts("^py-greenlet@0.4.17", when="@1.4.0:")
    depends_on("py-typing-extensions@4.2.0", when="@2:", type=("build", "run"))

    # >=1.4.0
    depends_on("py-mysqlclient@1.4:", when="backend=mysql @1.4:", type=("build", "run"))
    depends_on("py-psycopg2@2.7:", when="backend=postgresql @1.4:", type=("build", "run"))
    depends_on("py-pymysql", when="backend=pymysql @1.4:", type=("build", "run"))

    # < 1.4.0
    depends_on("py-mysqlclient", when="backend=mysql @:1.3", type=("build", "run"))
    depends_on("py-pymysql", when="backend=pymysql @:1.3", type=("build", "run"))
    depends_on("py-psycopg2", when="backend=postgresql @:1.3", type=("build", "run"))
