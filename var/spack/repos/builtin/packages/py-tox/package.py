# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTox(PythonPackage):
    """tox is a generic virtualenv management and test command line tool."""

    homepage = "https://tox.readthedocs.org/"
    pypi = "tox/tox-3.14.2.tar.gz"

    license("MIT")

    version("3.14.2", sha256="7efd010a98339209f3a8292f02909b51c58417bfc6838ab7eca14cf90f96117a")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-importlib-metadata@1.1.0:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-packaging@14:", type=("build", "run"))
    depends_on("py-pluggy@0.12.0:0", type=("build", "run"))
    depends_on("py-py@1.4.17:1", type=("build", "run"))
    depends_on("py-six@1.0.0:1", type=("build", "run"))
    depends_on("py-virtualenv@16.0.0:", type=("build", "run"))
    depends_on("py-toml@0.9.4:", type=("build", "run"))
    depends_on("py-filelock@3.0.0:3", type=("build", "run"))
