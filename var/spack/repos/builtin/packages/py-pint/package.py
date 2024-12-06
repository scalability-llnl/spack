# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPint(PythonPackage):
    """Pint is a Python package to define, operate and manipulate physical
    quantities: the product of a numerical value and a unit of measurement.
    It allows arithmetic operations between them and conversions from and
    to different units."""

    pypi = "pint/Pint-0.11.tar.gz"

    # 'pint' requires 'xarray', creating a circular dependency. Don't bother attempting
    # any import tests for this package.
    import_modules = []  # type: List[str]

    version("0.22", sha256="2d139f6abbcf3016cad7d3cec05707fe908ac4f99cf59aedfd6ee667b7a64433")
    version("0.21.1", sha256="5d5b6b518d0c5a7ab03a776175db500f1ed1523ee75fb7fafe38af8149431c8d")
    version("0.20.1", sha256="387cf04078dc7dfe4a708033baad54ab61d82ab06c4ee3d4922b1e45d5626067")
    version("0.19.2", sha256="e1d4989ff510b378dad64f91711e7bdabe5ca78d75b06a18569ac454678c4baf")
    version("0.18", sha256="8c4bce884c269051feb7abc69dbfd18403c0c764abc83da132e8a7222f8ba801")
    version("0.17", sha256="f4d0caa713239e6847a7c6eefe2427358566451fe56497d533f21fb590a3f313")
    version("0.11", sha256="308f1070500e102f83b6adfca6db53debfce2ffc5d3cbe3f6c367da359b5cf4d")
    version("0.10.1", sha256="d739c364b8326fe3d70773d5720fa8b005ea6158695cad042677a588480c86e6")
    version("0.10", sha256="38a4d6e242b8bab693cd83a5f5ade3d816463b498658e7ab14ce64c4d458c88b")
    version("0.9", sha256="32d8a9a9d63f4f81194c0014b3b742679dce81a26d45127d9810a68a561fe4e2")
    version("0.8.1", sha256="afcf31443a478c32bbac4b00337ee9026a13d0e2ac83d30c79151462513bb0d4")

    depends_on("python@3.9:", when="@0.22:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.19:0.21", type=("build", "run"))
    depends_on("py-typing-extensions", when="@0.22:", type=("build", "run"))
    depends_on("py-setuptools@61:", when="@0.21:", type="build")
    depends_on("py-setuptools@41:", when="@0.16:0.20", type="build")
    depends_on("py-setuptools@41:", when="@0.11:0.15", type=("build", "run"))
    depends_on("py-setuptools", when="@:0.10", type=("build", "run"))
    depends_on("py-setuptools-scm@3.4.3:+toml", when="@0.11:", type="build")
    depends_on("py-setuptools-scm", when="@0.10", type="build")
    depends_on("py-packaging", when="@0.13:18", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@0.13:18 ^python@:3.7", type=("build", "run"))
