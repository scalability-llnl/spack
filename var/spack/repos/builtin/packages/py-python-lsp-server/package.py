# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLspServer(PythonPackage):
    """A Python 3.7+ implementation of the Language Server Protocol."""

    homepage = "https://github.com/python-lsp/python-lsp-server"
    pypi = "python-lsp-server/python-lsp-server-1.6.0.tar.gz"

    maintainers("alecbcs")

    license("MIT")

    version("1.10.0", sha256="0c9a52dcc16cd0562404d529d50a03372db1ea6fb8dfcc3792b3265441c814f4")
    version("1.7.1", sha256="67473bb301f35434b5fa8b21fc5ed5fac27dc8a8446ccec8bae456af52a0aef6")
    version("1.7.0", sha256="401ce78ea2e98cadd02d94962eb32c92879caabc8055b9a2f36d7ef44acc5435")
    version("1.6.0", sha256="d75cdff9027c4212e5b9e861e9a0219219c8e2c69508d9f24949951dabd0dc1b")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"), when="@1.8.0:")
    depends_on("py-setuptools@61.2.0:", type=("build", "run"), when="@:1.7")
    depends_on("py-setuptools@61.2.0:", type="build", when="@1.8.0:")
    depends_on("py-setuptools-scm@3.4.3:+toml", type="build")

    depends_on("py-docstring-to-markdown", type=("build", "run"))
    depends_on("py-importlib-metadata@4.8.3:", type=("build", "run"), when="@1.8.0: ^python@:3.9")
    depends_on("py-jedi@0.17.2:0.18", type=("build", "run"), when="@:1.7")
    depends_on("py-jedi@0.17.2:0.19", type=("build", "run"), when="@1.8.0:")
    depends_on("py-pluggy@1.0.0:", type=("build", "run"))
    depends_on("py-python-lsp-jsonrpc@1.0.0:1", type=("build", "run"))
    depends_on("py-python-lsp-jsonrpc@1.1.0:1", type=("build", "run"), when="@1.8.0:")
    depends_on("py-ujson@3.0.0:", type=("build", "run"))
