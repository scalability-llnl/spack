# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypeguard(PythonPackage):
    """
    Run-time type checker for Python.
    """

    homepage = "https://github.com/agronholm/typeguard"
    pypi = "typeguard/typeguard-2.12.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("3.0.2", sha256="fee5297fdb28f8e9efcb8142b5ee219e02375509cd77ea9d270b5af826358d5a")
    version("2.13.3", sha256="00edaa8da3a133674796cf5ea87d9f4b4c367d77476e185e80251cc13dfbb8c4")
    version("2.12.1", sha256="c2af8b9bdd7657f4bd27b45336e7930171aead796711bc4cfc99b4731bb9d051")

    depends_on("python@3.5.3:", when="@:2.13.3", type=("build", "run"))
    depends_on("python@3.7.4:", when="@3.0.2:", type=("build", "run"))
    depends_on("py-setuptools@42:", when="@:2.13.3", type="build")
    depends_on("py-setuptools@64:", when="@3.0.2:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", when="@:2.13.3", type="build")
    depends_on("py-setuptools-scm@6.4:+toml", when="@3.0.2:", type="build")
    depends_on("py-importlib-metadata@3.6:", when="@3.0.2: ^python@:3.9", type=("build", "run"))
    depends_on("py-typing-extensions@4.4.0:", when="@3.0.2: ^python@:3.10", type=("build", "run"))
