# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAgateSql(PythonPackage):
    """agate-sql adds SQL read/write support to agate."""

    homepage = "https://agate-sql.readthedocs.io/en/latest/"
    pypi = "agate-sql/agate-sql-0.5.4.tar.gz"

    license("MIT")

    version("0.5.4", sha256="9277490ba8b8e7c747a9ae3671f52fe486784b48d4a14e78ca197fb0e36f281b")

    depends_on("py-setuptools", type="build")
    depends_on("py-agate@1.5.0:", type=("build", "run"))
    depends_on("py-sqlalchemy@1.0.8:", type=("build", "run"))
