# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlumDispatch(PythonPackage):
    """Multiple dispatch in Python."""

    homepage = "https://github.com/beartype/plum"
    pypi = "plum_dispatch/plum_dispatch-2.2.2.tar.gz"

    license("MIT")

    version("2.2.2", sha256="d5d180225c9fbf0277375bb558b649d97d0b651a91037bb7155cedbe9f52764b")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatchling@1.8.0:", type="build")
    depends_on("py-hatch-vcs", type="build")
    depends_on("py-beartype@0.16.2:", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.10", type=("build", "run"))
