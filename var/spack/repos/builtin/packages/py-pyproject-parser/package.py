# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyprojectParser(PythonPackage):
    """Parser for 'pyproject.toml'"""

    homepage = "https://github.com/repo-helper/pyproject-parser"
    pypi = "pyproject_parser/pyproject-parser-0.9.1.tar.gz"

    license("MIT")

    version("0.9.1", sha256="fa0b2ff78bc95788b08d00e1aafa66d3f7f3ab693f19d9c2e23e20000a69fd9b")

    depends_on("py-wheel@0.34.2:", type="build")
    depends_on("py-setuptools@40.6:", type="build")
    conflicts("^py-setuptools@61")
    depends_on("py-apeye-core@1:", type=("build", "run"))
    depends_on("py-attrs@20.3:", type=("build", "run"))
    depends_on("py-dom-toml@0.4:", type=("build", "run"))
    depends_on("py-domdf-python-tools@2.8:", type=("build", "run"))
    depends_on("py-natsort@7.1.1:", type=("build", "run"))
    depends_on("py-packaging@20.9:", type=("build", "run"))
    depends_on("py-shippinglabel@1:", type=("build", "run"))
    depends_on("py-toml@0.10.2:", type=("build", "run"))
    depends_on("py-tomli@1.2.3:", type=("build", "run"), when="^python@:3.10")
    depends_on("py-typing-extensions@3.7.4.3:", type=("build", "run"))
    conflicts("^py-typing-extensions@4.7.0")
