# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPyshacl(PythonPackage):
    """A Python validator for SHACL."""

    homepage = "https://github.com/RDFLib/pySHACL"
    pypi = "pyshacl/pyshacl-0.17.2.tar.gz"

    license("Apache-2.0")

    version("0.25.0", sha256="91e87ed04ccb29aa47abfcf8a3e172d35a8831fce23a011cfbf35534ce4c940b")
    version("0.20.0", sha256="47f014c52cc69167b902c89b3940dd400f7f5d2169a62f97f837f3419b4a737d")
    version("0.17.2", sha256="46f31c7a7f7298aa5b483d92dbc850ff79a144d26f1f41e83267ed84b4d6ae23")

    depends_on("py-poetry-core@1.1:1", type="build")
    depends_on("py-poetry-core@1.8.1:1", when="@0.25.0:", type="build")
    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("python@3.8.1:3", when="@0.25.0:", type=("build", "run"))
    depends_on("py-rdflib@6.0.0:6", when="@0.17.2", type=("build", "run"))
    depends_on("py-rdflib@6.2.0:6", when="@0.20.0", type=("build", "run"))
    depends_on("py-rdflib@6.3.2:7", when="@0.25.0:", type=("build", "run"))
    depends_on("py-html5lib@1.1:1", when="@0.20.0:", type=("build", "run"))
    depends_on("py-importlib-metadata@7:", when="@0.25.0: ^python@:3.11", type=("build", "run"))
    depends_on("py-owlrl@5.2.3:6", when="@0.17.2", type=("build", "run"))
    depends_on("py-owlrl@6.0.2:6", when="@0.20.0:", type=("build", "run"))
    depends_on("py-packaging@21.3:", when="@0.20.0:", type=("build", "run"))
    depends_on("py-prettytable@2.2.1:2", when="@:0.20", type=("build", "run"))
    depends_on("py-prettytable@3.5.0:", when="@0.25.0: ^python@:3.11", type=("build", "run"))
    depends_on("py-prettytable@3.7.0:", when="@0.25.0: ^python@3.12:", type=("build", "run"))

    def patch(self):
        if self.spec.satisfies("@0.17.2"):
            filter_file("^5.2.3,<7", ">=5.2.3,<7", "pyproject.toml", string=True)
