# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGimmik(PythonPackage):
    """Generator of Matrix Multiplication Kernels - GiMMiK - is a tool for generation of
    high performance matrix multiplication kernel code.
    for various accelerator platforms."""

    homepage = "https://github.com/PyFR/GiMMiK"
    pypi = "gimmik/gimmik-2.2.tar.gz"

    maintainers("MichaelLaufer")

    license("BSD-3-Clause")

    version("3.2.1", sha256="048644bd71497eb07e144f2c22fdee49ba23e1cde5fb954c3c30c4e3ea23687a")
    version("3.0", sha256="45c2da7acff3201b7796ba731e4be7f3b4f39469ff1f1bc0ddf4f19c4a6af010")
    version("2.3", sha256="c019c85316bcf0d5e84de9b7d10127355dfe8037c0e37f1880a9819ce92b74e1")
    version("2.2", sha256="9144640f94aab92f9c5dfcaf16885a79428ab97337cf503a4b2dddeb870f3cf0")

    depends_on("python@3.8", when="@:2.3", type=("build", "run"))
    depends_on("python@3.9:", when="@3.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-mako", type=("build", "run"))
