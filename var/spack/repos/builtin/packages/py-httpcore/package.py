# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpcore(PythonPackage):
    """The HTTP Core package provides a minimal low-level HTTP client,
    which does one thing only. Sending HTTP requests."""

    homepage = "https://github.com/encode/httpcore"
    pypi = "httpcore/httpcore-0.11.0.tar.gz"

    license("BSD-3-Clause")

    version("1.0.5", sha256="34a38e2f9291467ee3b44e89dd52615370e152954ba21721378a87b2960f7a61")
    version("0.18.0", sha256="13b5e5cd1dca1a6636a6aaea212b19f4f85cd88c366a2b82304181b769aab3c9")
    version("0.16.3", sha256="c5d6f04e2fc530f39e0c077e6a30caa53f1451096120f1f38b954afd0b17c0cb")
    version("0.14.7", sha256="7503ec1c0f559066e7e39bc4003fd2ce023d01cf51793e3c173b864eb456ead1")
    version("0.11.0", sha256="35ffc735d746b83f8fc6d36f82600e56117b9e8adc65d0c0423264b6ebfef7bf")

    depends_on("py-setuptools", when="@:1.16.3", type="build")
    depends_on("py-hatchling", when="@0.18:", type="build")
    depends_on("py-hatch-fancy-pypi-readme", when="@0.18:", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-certifi", when="@0.14.7:")

        depends_on("py-h11@0.8:0.9", when="@0.11.0")
        depends_on("py-h11@0.11:0.12", when="@0.14.7")
        depends_on("py-h11@0.13:0.14", when="@0.16.3:")

        depends_on("py-sniffio@1", when="@0")

        depends_on("py-anyio@3", when="@0.14.7")
        depends_on("py-anyio@3:4", when="@0.16.3:0.18")
