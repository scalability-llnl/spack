# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylcFlow(PythonPackage):
    """A workflow engine for cycling systems."""

    homepage = "https://cylc.org"
    pypi = "cylc-flow/cylc-flow-8.1.4.tar.gz"

    maintainers("LydDeb", "climbfuji")

    license("GPL-3.0-only")

    version("8.2.3", sha256="dd5bea9e4b8dad00edd9c3459a38fb778e5a073da58ad2725bc9b84ad718e073")
    version("8.2.0", sha256="cbe35e0d72d1ca36f28a4cebe9b9040a3445a74253bc94051a3c906cf179ded0")
    version("8.1.4", sha256="d1835ac18f6f24f3115c56b2bc821185484e834a86b12fd0033ff7e4dc3c1f63")

    depends_on("py-setuptools@49:66,68:", type=("build", "run"))
    depends_on("py-aiofiles@0.7", type=("build", "run"), when="@:8.1")
    depends_on("py-ansimarkup@1.0.0:", type=("build", "run"))
    depends_on("py-async-timeout@3.0.0:", type=("build", "run"))
    depends_on("py-colorama@0.4:1", type=("build", "run"))
    depends_on("py-graphene@2.1:2", type=("build", "run"))
    depends_on("py-jinja2@3.0", type=("build", "run"))
    depends_on("py-metomi-isodatetime@3.0", type=("build", "run"), when="@:8.2.0")
    depends_on("py-metomi-isodatetime@3:3.1", type=("build", "run"), when="@8.2.3:")
    depends_on("py-protobuf@4.21.2:4.21", type=("build", "run"))
    depends_on("py-psutil@5.6.0:", type=("build", "run"))
    depends_on("py-pyzmq@22:", type=("build", "run"), when="@8.2:")
    depends_on("py-pyzmq@22", type=("build", "run"), when="@:8.1")
    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.7")
    depends_on("py-urwid@2", type=("build", "run"))
    depends_on("py-rx", type=("build", "run"))
    depends_on("py-promise", type=("build", "run"))
    depends_on("py-tomli@2:", type=("build", "run"), when="^python@:3.10")

    # Non-Python dependencies
    depends_on("graphviz", type="run")
