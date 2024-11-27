# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUvloop(PythonPackage):
    """uvloop is a fast, drop-in replacement of the built-in asyncio event"""

    homepage = "https://github.com/MagicStack/uvloop"
    pypi = "uvloop/uvloop-0.14.0.tar.gz"

    license("Apache-2.0")

    version("0.19.0", sha256="0246f4fd1bf2bf702e06b0d45ee91677ee5c31242f39aab4ea6fe0c51aedd0fd")
    version("0.18.0", sha256="d5d1135beffe9cd95d0350f19e2716bc38be47d5df296d7cc46e3b7557c0d1ff")
    version("0.17.0", sha256="0ddf6baf9cf11a1a22c71487f39f15b2cf78eb5bde7e5b45fbb99e8a9d91b9e1")
    version("0.16.0", sha256="f74bc20c7b67d1c27c72601c78cf95be99d5c2cdd4514502b4f3eb0933ff1228")
    version("0.14.0", sha256="123ac9c0c7dd71464f58f1b4ee0bbd81285d96cdda8bc3519281b8973e3a461e")

    depends_on("c", type="build")  # generated

    depends_on("python@3.8:", when="@0.19:", type=("build", "run"))
    depends_on("python@3.7:", when="@0.15:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-setuptools@60:", when="@0.18:")
        depends_on("py-cython@0.29.36:0.29", when="@0.17:")  # May have been required for 0.16:
