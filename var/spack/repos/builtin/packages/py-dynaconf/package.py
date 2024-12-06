# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDynaconf(PythonPackage):
    """Dynaconf is a dynamic configuration management package for Python projects"""

    homepage = "https://github.com/dynaconf/dynaconf"
    pypi = "dynaconf/dynaconf-3.2.2.tar.gz"

    license("MIT")

    version("3.2.2", sha256="2f98ec85a2b8edb767b3ed0f82c6d605d30af116ce4622932a719ba70ff152fc")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@38.6.0:", type="build")
