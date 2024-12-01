# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySanic(PythonPackage):
    """Sanic is a Flask-like Python 3.5+ web server that is written to go fast.
    It is based on the work done by the amazing folks at magicstack"""

    homepage = "https://github.com/huge-success/sanic"
    pypi = "sanic/sanic-20.6.3.tar.gz"

    license("MIT")

    version("20.6.3", sha256="30e83d9f677b609d6b8ccab7c9551ca7e9a5f19ac0579f5aa10199ab6d4138ed")

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-ujson")
    depends_on("py-multidict@4.0:4")
    depends_on("py-aiofiles@0.3.0:")
    depends_on("py-httptools@0.0.10:")
    depends_on("py-websockets@8.1:8")
    depends_on("py-httpx@0.11.1")
    depends_on("py-websockets@8.1:8")
    depends_on("py-uvloop")
    depends_on("py-chardet")
    depends_on("py-hstspreload")
    depends_on("py-h2")
    depends_on("py-urllib3")
    depends_on("py-brotlipy")
