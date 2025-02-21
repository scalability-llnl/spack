# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTextx(PythonPackage):
    """Meta-language for DSL implementation inspired by Xtext."""

    homepage = "https://textx.github.io/textX/"
    pypi = "textx/textx-4.0.1.tar.gz"

    license("MIT")

    version("4.0.1", sha256="84aff5c95fd2c947402fcbe83eeeddc23aabcfed3464ab84184ef193c52d831a")

    depends_on("c", type="build")
    depends_on("py-flit-core@3.8:3", type="build")
    depends_on("python@3.8:3.12", type=("build", "run"))
    depends_on("py-arpeggio@2:", type=("build", "run"))
    depends_on("py-importlib-metadata", when="^python@:3.9", type=("build", "run"))
