# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLspJsonrpc(PythonPackage):
    """A Python 3.7+ server implementation of the JSON RPC 2.0 protocol."""

    homepage = "https://github.com/python-lsp/python-lsp-jsonrpc"
    pypi = "python-lsp-jsonrpc/python-lsp-jsonrpc-1.0.0.tar.gz"

    maintainers("alecbcs")

    license("MIT")

    version("1.1.2", sha256="4688e453eef55cd952bff762c705cedefa12055c0aec17a06f595bcc002cc912")
    version("1.0.0", sha256="7bec170733db628d3506ea3a5288ff76aa33c70215ed223abdb0d95e957660bd")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@61.2.0:", type="build", when="@1.1.0:")
    depends_on("py-setuptools-scm@3.4.3:+toml", type="build", when="@1.1.0:")

    depends_on("py-ujson@3.0.0:", type=("build", "run"))
