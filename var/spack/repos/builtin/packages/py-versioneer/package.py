# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVersioneer(PythonPackage):
    """Versioneer is a tool to automatically update version strings by
    asking your version-control system about the current tree."""

    homepage = "https://github.com/python-versioneer/python-versioneer"
    pypi = "versioneer/versioneer-0.26.tar.gz"
    git = "https://github.com/python-versioneer/python-versioneer.git"

    maintainers("scemama")

    license("Unlicense")

    version("0.29", sha256="5ab283b9857211d61b53318b7c792cf68e798e765ee17c27ade9f6c924235731")
    version("0.28", sha256="7175ca8e7bb4dd0e3c9779dd2745e5b4a6036304af3f5e50bd896f10196586d6")
    version("0.27", sha256="452e0130658e9d3f0ba3e8a70cf34ef23c0ff6cbf743555b3e73a6c11d0161a3")
    version("0.26", sha256="84fc729aa296d1d26645a8f62f178019885ff6f9a1073b29a4a228270ac5257b")
    version("0.18", sha256="ead1f78168150011189521b479d3a0dd2f55c94f5b07747b484fd693c3fbf335")

    depends_on("c", type="build")  # generated

    variant("toml", default=True, description="Install TOML support", when="@0.26:")

    depends_on("py-setuptools", type="build")
    depends_on("py-tomli", when="@0.28: ^python@:3.10", type="build")
    depends_on("py-tomli", when="@0.27", type="build")

    depends_on("py-tomli", when="@0.28: +toml ^python@:3.10", type=("build", "run"))
    depends_on("py-tomli", when="@:0.27 +toml", type=("build", "run"))
