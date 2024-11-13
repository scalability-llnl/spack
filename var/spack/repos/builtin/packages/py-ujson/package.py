# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUjson(PythonPackage):
    """Ultra fast JSON decoder and encoder written in C with Python
    bindings."""

    homepage = "https://github.com/esnme/ultrajson"
    pypi = "ujson/ujson-1.35.tar.gz"

    version("5.7.0", sha256="e788e5d5dcae8f6118ac9b45d0b891a0d55f7ac480eddcb7f07263f2bcf37b23")
    version("4.0.2", sha256="c615a9e9e378a7383b756b7e7a73c38b22aeb8967a8bfbffd4741f7ffd043c4d")
    version("1.35", sha256="f66073e5506e91d204ab0c614a148d5aa938bdbf104751be66f8ad7a222f5f86")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@42:", when="@5:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", when="@5:", type="build")
    depends_on("py-setuptools-scm", when="@4:", type="build")
