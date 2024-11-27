# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAutopep8(PythonPackage):
    """autopep8 automatically formats Python code to conform to the
    PEP 8 style guide."""

    homepage = "https://github.com/hhatto/autopep8"
    pypi = "autopep8/autopep8-1.2.4.tar.gz"

    license("MIT")

    version("1.7.0", sha256="ca9b1a83e53a7fad65d731dc7a2a2d50aa48f43850407c59f6a1a306c4201142")
    version("1.6.0", sha256="44f0932855039d2c15c4510d6df665e4730f2b8582704fa48f9c55bd3e17d979")
    version("1.5.7", sha256="276ced7e9e3cb22e5d7c14748384a5cf5d9002257c0ed50c0e075b68011bb6d0")
    version("1.4.4", sha256="4d8eec30cc81bc5617dbf1218201d770dc35629363547f17577c61683ccfb3ee")
    version("1.3.3", sha256="ff787bffb812818c3071784b5ce9a35f8c481a0de7ea0ce4f8b68b8788a12f30")

    depends_on("py-pycodestyle@2.3.0:", when="@1.3:", type=("build", "run"))
    depends_on("py-pycodestyle@2.4.0:", when="@1.4:", type=("build", "run"))
    depends_on("py-pycodestyle@2.7.0:", when="@1.5.6:", type=("build", "run"))
    depends_on("py-pycodestyle@2.8.0:", when="@1.6.0:", type=("build", "run"))
    depends_on("py-pycodestyle@2.9.1:", when="@1.7.0:", type=("build", "run"))

    depends_on("py-toml", when="@1.5.3:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
