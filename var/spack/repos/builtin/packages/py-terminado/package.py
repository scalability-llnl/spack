# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTerminado(PythonPackage):
    """Terminals served to term.js using Tornado websockets"""

    homepage = "https://github.com/jupyter/terminado"
    pypi = "terminado/terminado-0.8.3.tar.gz"

    version("0.17.1", sha256="6ccbbcd3a4f8a25a5ec04991f39a0b8db52dfcd487ea0e578d977e6752380333")
    version("0.15.0", sha256="ab4eeedccfcc1e6134bfee86106af90852c69d602884ea3a1e8ca6d4486e9bfe")
    version("0.12.1", sha256="b20fd93cc57c1678c799799d117874367cc07a3d2d55be95205b1a88fa08393f")
    version("0.8.3", sha256="4804a774f802306a7d9af7322193c5390f1da0abb429e082a10ef1d46e6fb2c2")
    version("0.8.2", sha256="de08e141f83c3a0798b050ecb097ab6259c3f0331b2f7b7750c9075ced2c20c2")
    version("0.8.1", sha256="55abf9ade563b8f9be1f34e4233c7b7bde726059947a593322e8a553cc4c067a")
    version("0.6", sha256="2c0ba1f624067dccaaead7d2247cfe029806355cef124dc2ccb53c83229f0126")

    depends_on("py-hatchling@1.5:", when="@0.16:", type="build")
    depends_on("py-hatchling@0.25:", when="@0.15:", type="build")

    depends_on("py-ptyprocess", type=("build", "run"))
    depends_on("py-tornado@6.1.0:", when="@0.15:", type=("build", "run"))
    depends_on("py-tornado@4:", type=("build", "run"))
    # not yet in spack
    # depends_on("py-pywinpty@1.1:", when="platform=windows", type=("build", "run"))

    # Historical dependencies
    depends_on("py-setuptools@40.8.0:", when="@0.12.1", type="build")
    depends_on("py-flit", when="@0.8", type="build")
    depends_on("py-setuptools", when="@:0.6", type="build")
