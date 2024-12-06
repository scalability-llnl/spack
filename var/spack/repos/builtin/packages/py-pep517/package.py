# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPep517(PythonPackage):
    """Wrappers to build Python packages using PEP 517 hooks."""

    homepage = "https://github.com/pypa/pep517"
    pypi = "pep517/pep517-0.12.0.tar.gz"

    license("MIT")

    version("0.12.0", sha256="931378d93d11b298cf511dd634cf5ea4cb249a28ef84160b3247ee9afb4e8ab0")

    depends_on("py-flit-core@2:3", type="build")
    depends_on("py-tomli@1.1:", when="^python@3.6:", type=("build", "run"))
    depends_on("py-importlib-metadata", when="^python@:3.7", type=("build", "run"))
    depends_on("py-zipp", when="^python@:3.7", type=("build", "run"))
