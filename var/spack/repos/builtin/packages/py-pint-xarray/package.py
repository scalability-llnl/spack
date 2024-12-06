# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPintXarray(PythonPackage):
    """A convenience wrapper for using pint with xarray"""

    homepage = "https://github.com/xarray-contrib/pint-xarray"
    pypi = "pint-xarray/pint-xarray-0.2.1.tar.gz"

    license("Apache-2.0")

    version("0.3", sha256="3545dfa78bee3f98eba29b8bd17500e3b5cb7c7b03a2c2781c4d4d59b6a82841")
    version("0.2.1", sha256="1ee6bf74ee7b52b946f226a96469276fa4f5c68f7381c1b2aae66852562cb275")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")

    depends_on("python@3.8:", when="@0.3:", type=("build", "run"))
    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-xarray@0.16.1:", type=("build", "run"))
    depends_on("py-pint@0.16:", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@0.2.1 ^python@:3.7", type=("build", "run"))
