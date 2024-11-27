# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyUtil(PythonPackage):
    """Galaxy Generic Utilities"""

    homepage = "https://github.com/galaxyproject/galaxy"
    pypi = "galaxy-util/galaxy-util-22.1.2.tar.gz"

    license("CC-BY-3.0")

    version("22.1.2", sha256="80257c94dc9122ebf80d643aa3962fe8beda23dbba8fc4820a0d2b720f479f98")

    depends_on("py-setuptools", type="build")

    depends_on("py-bleach", type=("build", "run"))
    depends_on("py-boltons", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-importlib-resources", type=("build", "run"))
    depends_on("py-markupsafe", type=("build", "run"))
    depends_on("py-packaging@:21", type=("build", "run"))
    depends_on("py-pycryptodome", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-routes", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-zipstream-new", type=("build", "run"))
