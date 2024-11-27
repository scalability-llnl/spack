# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOrjson(PythonPackage):
    """Fast, correct Python JSON library supporting dataclasses, datetimes, and numpy."""

    homepage = "https://github.com/ijl/orjson"
    pypi = "orjson/orjson-3.8.7.tar.gz"

    license("Apache-2.0")

    version("3.10.3", sha256="2b166507acae7ba2f7c315dcf185a9111ad5e992ac81f2d507aac39193c2c818")
    version("3.9.15", sha256="95cae920959d772f30ab36d3b25f83bb0f3be671e986c72ce22f8fa700dae061")
    version("3.8.14", sha256="5ea93fd3ef7be7386f2516d728c877156de1559cda09453fc7dd7b696d0439b3")
    version("3.8.7", sha256="8460c8810652dba59c38c80d27c325b5092d189308d8d4f3e688dbd8d4f3b2dc")

    depends_on("c", type="build")  # generated

    with default_args(type="build"):
        with when("@3.8"):
            depends_on("rust@1.60:")
            depends_on("python@3.7:")
            depends_on("py-maturin@0.13:0.14")
        with when("@03.9:"):
            depends_on("rust@1.72:")
            depends_on("python@3.8:")
            depends_on("py-maturin@1")
