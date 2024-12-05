# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLazyarray(PythonPackage):
    """a Python package that provides a lazily-evaluated numerical array class,
    larray, based on and compatible with NumPy arrays."""

    homepage = "https://lazyarray.readthedocs.io/en/latest/"
    pypi = "lazyarray/lazyarray-0.2.8.tar.gz"

    license("BSD-3-Clause")

    version("0.5.2", sha256="fe31804d82115ed7c382840a1708f498419ec1455cac084707ece9908310c7d1")
    version("0.5.1", sha256="76964dd1384a6d020ae0e70806983d15d8fcd731734063f716696ebe300ab0af")
    version("0.5.0", sha256="4cc4b54940def52fd96818a1c10528c4b7ecca77aa617d9e4fecfb42b51e73cf")
    version("0.4.0", sha256="837cfe001840be43339d4c10d0028a70a8b3c22be08b75429a38472cbf327976")
    version("0.3.4", sha256="357e80db7472c940ed3cab873544f2b7028f6ade8737adde2c91f91aeab2835a")
    version("0.3.3", sha256="c9df003af5e1007a28c4ec45f995662fd195590d5694ef7d4cfb028bc508f6ed")
    version("0.3.2", sha256="be980534c5950a976709085570f69be9534bdf0f3e5c21a9113de3ee2052683e")
    version("0.2.10", sha256="7a53f81b5f3a098c04003d2ad179fc197451fd96bc921510f8534c6af8cc8e19")
    version("0.2.8", sha256="aaee4e18117cc512de7a4e64522f37bc6f4bf125ecffdbdbf4e4e390fbdd9ba2")

    # Required versions come from doc/installation.txt or:
    # https://lazyarray.readthedocs.io/en/latest/installation.html#dependencies
    depends_on("python@2.7:3.9", type=("build", "run"), when="@0.3:0.3.4")
    depends_on("python@3.4:3.9", type=("build", "run"), when="@0.4:0.5.1")
    depends_on("python@3.6:", type=("build", "run"), when="@0.5.2:")
    depends_on("py-numpy@1.5:", type=("build", "run"), when="@:0.2.10")
    depends_on("py-numpy@1.12:", type=("build", "run"), when="@0.3:0.5.1")
    depends_on("py-numpy@1.13:", type=("build", "run"), when="@0.5.2:")

    depends_on("py-setuptools", type="build")
