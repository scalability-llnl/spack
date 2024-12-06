# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribWebsupport(PythonPackage):
    """sphinxcontrib-webuspport provides a Python API to easily integrate
    Sphinx documentation into your Web application."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-websupport/sphinxcontrib-websupport-1.1.2.tar.gz"

    license("BSD-2-Clause")

    version("1.1.2", sha256="1501befb0fdf1d1c29a800fdbf4ef5dc5369377300ddbdd16d2cd40e54c6eefc")
    version("1.1.0", sha256="9de47f375baf1ea07cdb3436ff39d7a9c76042c10a769c52353ec46e4e8fc3b9")
    version("1.0.1", sha256="7a85961326aa3a400cd4ad3c816d70ed6f7c740acd7ce5d78cd0a67825072eb9")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
