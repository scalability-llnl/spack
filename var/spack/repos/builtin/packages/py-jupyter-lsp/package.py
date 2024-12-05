# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterLsp(PythonPackage):
    """Multi-Language Server WebSocket proxy for Jupyter Notebook/Lab server."""

    homepage = "https://github.com/jupyter-lsp/jupyterlab-lsp"
    pypi = "jupyter-lsp/jupyter-lsp-2.2.0.tar.gz"

    license("BSD-3-Clause")

    version("2.2.0", sha256="8ebbcb533adb41e5d635eb8fe82956b0aafbf0fd443b6c4bfa906edeeb8635a1")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-jupyter-server@1.1.2:", type=("build", "run"))
    depends_on("py-importlib-metadata@4.8.3:", when="^python@:3.9", type=("build", "run"))
