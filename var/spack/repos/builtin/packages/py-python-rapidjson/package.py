# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonRapidjson(PythonPackage):
    """Python wrapper around rapidjson."""

    homepage = "https://github.com/python-rapidjson/python-rapidjson"
    pypi = "python-rapidjson/python-rapidjson-0.9.1.tar.gz"

    license("MIT")

    version("1.10", sha256="acfecbf5edb91ec72a20a125de7f56b8c2f6161eff4c65382c8ee6a2484d3540")
    version("1.9", sha256="be7d351c7112dac608133a23f60e95395668d0981a07f4037f63e0e88afcf01a")
    version("1.8", sha256="170c2ff97d01735f67afd0e1cb0aaa690cb69ae6016e020c6afd5e0ab9b39899")
    version("1.5", sha256="04323e63cf57f7ed927fd9bcb1861ef5ecb0d4d7213f2755969d4a1ac3c2de6f")
    version("0.9.1", sha256="ad80bd7e4bb15d9705227630037a433e2e2a7982b54b51de2ebabdd1611394a1")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.4:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@1.5:")
    depends_on("py-setuptools", type="build")
