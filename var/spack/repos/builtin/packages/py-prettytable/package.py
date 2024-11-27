# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPrettytable(PythonPackage):
    """PrettyTable is a simple Python library designed to make
    it quick and easy to represent tabular data in visually
    appealing ASCII tables.
    """

    homepage = "https://github.com/jazzband/prettytable"
    pypi = "prettytable/prettytable-0.7.2.tar.gz"

    version("3.7.0", sha256="ef8334ee40b7ec721651fc4d37ecc7bb2ef55fde5098d994438f0dfdaa385c0c")
    version("3.4.1", sha256="7d7dd84d0b206f2daac4471a72f299d6907f34516064feb2838e333a4e2567bd")
    version("3.2.0", sha256="ae7d96c64100543dc61662b40a28f3b03c0f94a503ed121c6fca2782c5816f81")
    version("2.4.0", sha256="18e56447f636b447096977d468849c1e2d3cfa0af8e7b5acfcf83a64790c0aca")
    version("2.2.1", sha256="6d465005573a5c058d4ca343449a5b28c21252b86afcdfa168cdc6a440f0b24c")
    version("0.7.2", sha256="2d5460dc9db74a32bcc8f9f67de68b2c4f4d2f01fa3bd518764c69156d9cacd9")

    depends_on("py-setuptools", type="build", when="@:3.4")
    depends_on("py-hatchling", type="build", when="@3.7:")
    depends_on("py-hatch-vcs", type="build", when="@3.7:")
    depends_on("py-wcwidth", type=("build", "run"), when="@2.4.0:")
    depends_on("py-importlib-metadata", type=("build", "run"), when="@2: ^python@:3.7")
    depends_on("py-setuptools-scm", type="build", when="@2.4.0:3.4")
