# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySqlparse(PythonPackage):
    """A non-validating SQL parser module for Python."""

    homepage = "https://github.com/andialbrecht/sqlparse"
    url = "https://github.com/andialbrecht/sqlparse/archive/0.3.1.tar.gz"

    license("BSD-3-Clause")

    version("0.5.1", sha256="a9f1a42ca749a019aa98d996b58e917f4c9e1b9ff164610355f35248733767bb")
    version("0.4.1", sha256="f75cdec98a4cc8296890279d744e1ae8618bb14dbad77e3d0637f0d7bb5d6535")
    version("0.3.1", sha256="344b539482b75c244ac69fbb160d0f4d63a288a392475c8418ca692c594561f9")
    version("0.3.0", sha256="a75fddae009fba1d66786203c9dd3a842aa4415475c466d15484139117108474")
    version("0.2.4", sha256="7087a2bd385c06ac1a5cf343e2e5ea7ce2bb6386849e59ef214e02af68f73fb4")
    version("0.2.3", sha256="12470ab41df1a7003a2957a79c6da9cd4ded180c8a193aa112fe0899b935ef30")

    depends_on("py-setuptools", type="build")
    depends_on("py-hatchling", when="@0.5.1:", type="build")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.5.1:", type=("build", "run"))
