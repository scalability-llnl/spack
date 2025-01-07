# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOracledb(PythonPackage):
    """Python-oracledb is the new name for the Python cx_Oracle driver.
    The python-oracledb driver is an open source module that enables
    Python programs to access Oracle Database."""

    homepage = "https://oracle.github.io/python-oracledb/"
    pypi = "oracledb/oracledb-1.4.2.tar.gz"

    license("Apache-2.0")

    version("2.4.1", sha256="bd5976bef0e466e0f9d1b9f6531fb5b8171dc8534717ccb04b26e680b6c7571d")
    version("2.3.0", sha256="b9b0c4ec280b10063e6789bed23ddc2435ae98569ebe64e0b9a270780b9103d5")
    version("1.4.2", sha256="e28ed9046f2735dc2dd5bbcdf3667f284e384e0ec7eed3eeb3798fa8a7d47e36")

    depends_on("python@3.8:3.13", when="@2.4:")
    depends_on("python@3.8:3.12", when="@2.0:2.3")
    depends_on("python@3.8:3.11", when="@:1.4")

    depends_on("c", type="build")

    depends_on("py-setuptools@40.6.0:", type="build")
    depends_on("py-cryptography@3.2.1:", type=("build", "run"))
    depends_on("py-cython@3:", type="build")
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("oracle-instant-client", type="run", when="impl=thick")

    variant(
        "impl",
        default="thick",
        description="Client Implementation",
        values=("thick", "thin"),
        multi=False,
    )
