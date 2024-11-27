# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestHttpbin(PythonPackage):
    """Easily test your HTTP library against a local copy of httpbin"""

    homepage = "https://github.com/kevin1024/pytest-httpbin"
    pypi = "pytest-httpbin/pytest-httpbin-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="d8ce547f42423026550ed7765f6c6d50c033b43025e8592270a7abf970e19b72")
    version("0.2.3", sha256="c5b698dfa474ffc9caebcb35e34346b753eb226aea5c2e1b69fefedbcf161bf8")
    version("0.0.7", sha256="03af8a7055c8bbcb68b14d9a14c103c82c97aeb86a8f1b29cd63d83644c2f021")

    depends_on("py-setuptools", type="build")
    depends_on("py-flask", when="@:0.2", type=("build", "run"))
    depends_on("py-decorator", when="@:0.2", type=("build", "run"))
    depends_on("py-httpbin", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
