# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy(PythonPackage):
    """Library with cross-python path, ini-parsing, io, code, log facilities"""

    homepage = "https://py.readthedocs.io/en/latest/"
    pypi = "py/py-1.8.0.tar.gz"

    license("MIT")

    version("1.11.0", sha256="51c75c4126074b472f746a24399ad32f6053d1b34b68d2fa41e558e6f4a98719")
    version("1.9.0", sha256="9ca6883ce56b4e8da7e79ac18787889fa5206c79dcc67fb065376cd2fe03f342")
    version("1.8.2", sha256="f3b3a4c36512a4c4f024041ab51866f11761cc169670204b235f6b20523d4e6b")
    version("1.8.0", sha256="dc639b046a6e2cff5bbe40194ad65936d6ba360b52b3c3fe1d08a82dd50b5e53")
    version("1.5.4", sha256="3fd59af7435864e1a243790d322d763925431213b6b8529c6ca71081ace3bbf7")
    version("1.5.3", sha256="29c9fab495d7528e80ba1e343b958684f4ace687327e6f789a94bf3d1915f881")
    version("1.4.33", sha256="1f9a981438f2acc20470b301a07a496375641f902320f70e31916fe3377385a9")
    version("1.4.31", sha256="a6501963c725fc2554dabfece8ae9a8fb5e149c0ac0a42fd2b02c5c1c57fc114")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"), when="@1.11.0:")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-setuptools-scm+toml", type="build", when="@1.11.0:")
