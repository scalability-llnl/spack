# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOracledb(PythonPackage):
    """Python-oracledb is the new name for the Python cx_Oracle driver.
    The python-oracledb driver is an open source module that enables
    Python programs to access Oracle Database."""

    homepage = "https://oracle.github.io/python-oracledb/"
    pypi = "oracledb/oracledb-1.2.2.tar.gz"

    license("Apache-2.0")

    version("1.2.2", sha256="dd9f63084e44642b484a46b2fcfb4fc921f39facf494a1bab00628fa6409f4fc")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@40.6.0:", type="build")
    depends_on("py-cryptography@3.2.1:", type=("build", "run"))
    depends_on("py-cython", type="build")
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("oracle-instant-client", type="run", when="impl=thick")

    variant(
        "impl",
        default="thick",
        description="Client Implementation",
        values=("thick", "thin"),
        multi=False,
    )
