# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxautomodapi(PythonPackage):
    """Provides Sphinx directives to autogenerate API documentation pages"""

    homepage = "https://sphinx-automodapi.readthedocs.io/en/latest/"
    pypi = "sphinx-automodapi/sphinx-automodapi-0.9.tar.gz"

    license("BSD-3-Clause")

    version("0.9", sha256="71a69e1a7ab8d849f416d7431db854d7b1925f749ba6345bc7d88f288892871d")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx@1.3:", type=("build", "run"))
