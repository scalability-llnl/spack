# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebargs(PythonPackage):
    """Python library for parsing and validating HTTP request objects,
    with built-in support for popular web frameworks, including Flask,
    Django, Bottle, Tornado, Pyramid, Falcon, and aiohttp."""

    homepage = "https://github.com/marshmallow-code/webargs"
    pypi = "webargs/webargs-8.1.0.tar.gz"

    maintainers("haralmha")

    license("MIT")

    version("8.1.0", sha256="f1f0b7f054a22263cf750529fc0926709ca47da9a2c417d423ad88d9fa6a5d33")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-marshmallow@3.0.0:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
