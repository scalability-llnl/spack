# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTemplateflow(PythonPackage):
    """A python client to query TemplateFlow via pyBIDS."""

    homepage = "https://github.com/templateflow/python-client"
    pypi = "templateflow/templateflow-0.7.1.tar.gz"

    license("Apache-2.0")

    version("0.7.1", sha256="c6e8282d1ffbb5dca7bd704a12e02bd00021860b71a043c35716861910c7187f")
    version("0.4.2", sha256="5585f3e7ccaa756f811aafb526ed6b2c79aabfd012477129af9c6038d7686f84")

    depends_on("python@3.6:", when="@0.5:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@40.9:", when="@0.7.1:", type="build")
    depends_on("py-setuptools@30.3:", type="build")
    depends_on("py-setuptools-scm+toml@3.4:", when="@0.6:", type="build")
    depends_on("py-wheel", when="@0.7.1", type="build")
    depends_on("py-pybids@0.12.1:", when="@0.6.3:", type=("build", "run"))
    depends_on("py-pybids@0.9.2:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
