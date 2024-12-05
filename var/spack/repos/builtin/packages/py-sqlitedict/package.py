# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySqlitedict(PythonPackage):
    """Persistent dict in Python, backed up by sqlite3 and pickle, multithread-safe."""

    homepage = "https://github.com/piskvorky/sqlitedict"
    pypi = "sqlitedict/sqlitedict-2.1.0.tar.gz"

    license("Apache-2.0")

    version("2.1.0", sha256="03d9cfb96d602996f1d4c2db2856f1224b96a9c431bdd16e78032a72940f9e8c")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
