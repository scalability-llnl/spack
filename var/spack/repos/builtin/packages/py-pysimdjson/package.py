# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysimdjson(PythonPackage):
    """Python bindings for the simdjson project, a SIMD-accelerated
    JSON parser. If SIMD instructions are unavailable a fallback parser
    is used, making pysimdjson safe to use anywhere."""

    homepage = "https://github.com/TkTech/pysimdjson"
    pypi = "pysimdjson/pysimdjson-4.0.3.tar.gz"

    maintainers("haralmha")

    license("MIT")

    version("4.0.3", sha256="61900992d7f992b073a8c5f93cafa4af9bfd3209624baa775699b0fdd6f67517")
    version("3.2.0", sha256="643baa0941752367761dbc091bf552bf4ca196cf67bf41ef89c90c2db2ec1477")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"), when="@4.0.3:")
    depends_on("python@3.5:", type=("build", "run"), when="@:4.0.2")
    depends_on("py-setuptools", type="build")
    depends_on("py-pybind11", when="@:3")
