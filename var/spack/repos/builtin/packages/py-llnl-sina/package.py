# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyLlnlSina(PythonPackage):
    """Sina allows codes to store, query, and visualize their data through an
    easy-to-use Python API. Data that fits its recognized schema can be ingested
    into one or more supported backends.
    Sina's API is independent of backend and gives users the benefits of a database
    without requiring knowledge of one, allowing queries to be expressed in pure
    Python.  Visualizations are also provided through Python.

    Sina is intended especially for use with run metadata,
    allowing users to easily and efficiently find simulation runs that match some
    criteria.
    """

    homepage = "https://github.com/LLNL/Sina"
    git = "https://github.com/LLNL/Sina.git"

    # notify when the package is updated.

    license("MIT")

    maintainers("HaluskaR", "estebanpauli", "murray55", "doutriaux1")
    version("1.11.0", tag="v1.11.0", commit="f3e9bb3a122cfae2a9fd82c3c5613cff939d3aa1")
    version("1.10.0", tag="v1.10.0", commit="9c3c0acca5f0d4ac02470571688f00ab0bd61a30")

    depends_on("cxx", type="build")  # generated

    # let's remove dependency on orjson
    patch("no_orjson.patch")
    depends_on("py-setuptools", type="build")
    depends_on("py-ujson", type=("build", "run"))
    depends_on("py-sqlalchemy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))

    build_directory = "python"
