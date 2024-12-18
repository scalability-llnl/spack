# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPluggy(PythonPackage):
    """Plugin and hook calling mechanisms for python."""

    homepage = "https://github.com/pytest-dev/pluggy"
    pypi = "pluggy/pluggy-0.13.0.tar.gz"

    license("MIT")

    version("1.5.0", sha256="2cffa88e94fdc978c4c574f15f9e59b7f4201d439195c3715ca9e2486f1d0cf1")
    version("1.4.0", sha256="8c85c2876142a764e5b7548e7d9a0e0ddb46f5185161049a79b7e974454223be")
    version("1.0.0", sha256="4224373bacce55f955a878bf9cfa763c1e360858e330072059e10bad68531159")
    version("0.13.0", sha256="fa5fa1622fa6dd5c030e9cad086fa19ef6a0cf6d7a2d12318e10cb49d6d68f34")
    version("0.12.0", sha256="0825a152ac059776623854c1543d65a4ad408eb3d33ee114dff91e57ec6ae6fc")
    version("0.9.0", sha256="19ecf9ce9db2fce065a7a0586e07cfb4ac8614fe96edf628a264b1c70116cf8f")
    version("0.8.1", sha256="8ddc32f03971bfdf900a81961a48ccf2fb677cf7715108f85295c67405798616")
    version("0.7.1", sha256="95eb8364a4708392bae89035f45341871286a333f749c3141c20573d2b3876e1")
    version("0.6.0", sha256="7f8ae7f5bdf75671a718d2daf0a64b7885f74510bcd98b1a0bb420eb9a9d0cff")

    with default_args(type="build"):
        depends_on("py-setuptools@45:", when="@1.1:")
        depends_on("py-setuptools")
        depends_on("py-setuptools-scm@6.2.3:+toml", when="@1.1:")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@1.3:")
        depends_on("python@3.7:", when="@1.1:")
        depends_on("py-importlib-metadata@0.12:", when="^python@:3.7")
