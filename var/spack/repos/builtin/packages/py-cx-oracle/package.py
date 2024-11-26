# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCxOracle(PythonPackage):
    """Python interface to Oracle"""

    homepage = "https://oracle.github.io/python-cx_Oracle"
    pypi = "cx_Oracle/cx_Oracle-8.3.0.tar.gz"

    version("8.3.0", sha256="3b2d215af4441463c97ea469b9cc307460739f89fdfa8ea222ea3518f1a424d9")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("oracle-instant-client", type="run")
    depends_on("py-setuptools@40.6.0:", type="build")
    depends_on("py-wheel", type="build")
