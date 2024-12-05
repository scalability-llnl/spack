# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJson5(PythonPackage):
    """The JSON5 Data Interchange Format (JSON5) is a superset of JSON that aims
    to alleviate some of the limitations of JSON by expanding its syntax to
    include some productions from ECMAScript 5.1."""

    homepage = "https://github.com/dpranke/pyjson5"
    pypi = "json5/json5-0.9.4.tar.gz"

    license("Apache-2.0")

    version("0.9.14", sha256="9ed66c3a6ca3510a976a9ef9b8c0787de24802724ab1860bc0153c7fdd589b02")
    version("0.9.10", sha256="ad9f048c5b5a4c3802524474ce40a622fae789860a86f10cc4f7e5f9cf9b46ab")
    version("0.9.6", sha256="9175ad1bc248e22bb8d95a8e8d765958bf0008fef2fe8abab5bc04e0f1ac8302")
    version("0.9.4", sha256="2ebfad1cd502dca6aecab5b5c36a21c732c3461ddbc412fb0e9a52b07ddfe586")

    depends_on("py-setuptools", type="build")
