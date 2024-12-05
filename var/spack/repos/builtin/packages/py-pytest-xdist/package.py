# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestXdist(PythonPackage):
    """py.test xdist plugin for distributed testing and loop-on-failing mode"""

    homepage = "https://github.com/pytest-dev/pytest-xdist"
    pypi = "pytest-xdist/pytest-xdist-3.2.0.tar.gz"

    license("MIT")

    version("3.2.0", sha256="fa10f95a2564cd91652f2d132725183c3b590d9fdcdec09d3677386ecf4c1ce9")
    version("1.30.0", sha256="5d1b1d4461518a6023d56dab62fb63670d6f7537f23e2708459a557329accf48")
    version("1.29.0", sha256="3489d91516d7847db5eaecff7a2e623dba68984835dbe6cedb05ae126c4fb17f")
    version("1.27.0", sha256="a96ed691705882560fa3fc95531fbd4c224896c827f4004817eb2dcac4ba41a2")
    version("1.24.0", sha256="8e188d13ce6614c7a678179a76f46231199ffdfe6163de031c17e62ffa256917")
    version("1.17.0", sha256="e7e48c111677af23078b1ed23501e493e12c4b6d91657f6884a64e4ce0f14144")
    version("1.16.0", sha256="42e5a1e5da9d7cff3e74b07f8692598382f95624f234ff7e00a3b1237e0feba2")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools@45.0:", type="build", when="@3.2.0:")
    depends_on("py-setuptools", type="build", when="@:1.30.0")
    depends_on("py-setuptools-scm@6.2.3: +toml", type="build", when="@3.2.0:")
    depends_on("py-execnet@1.1:", type=("build", "run"))
    depends_on("py-pytest@6.2.0:", type=("build", "run"), when="@3.2.0:")
    depends_on("py-pytest@4.4.0:", type=("build", "run"), when="@1.28.0:1.30.0")
    depends_on("py-pytest@3.6.0:", type=("build", "run"), when="@1.25.0:1.27.0")
    depends_on("py-pytest@3.0.0:", type=("build", "run"), when="@1.18.0:1.24.0")
    depends_on("py-pytest@2.7.0:", type=("build", "run"), when="@1.16.0:1.17.0")
    depends_on("py-pytest-forked", type=("build", "run"), when="@1.19.0:1")
    depends_on("py-six", type=("build", "run"), when="@1.23.0:1")
