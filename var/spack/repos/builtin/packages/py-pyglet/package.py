# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyPyglet(PythonPackage):
    """pyglet is a cross-platform windowing and multimedia library for Python
    for developing games and other visually rich applications.
    """

    homepage = "https://github.com/pyglet/pyglet"
    pypi = "pyglet/pyglet-2.0.9.zip"

    license("BSD-3-Clause")

    version("2.0.10", sha256="242beb1b3bd67c5bebdfe5ba11ec56b696ad86b50c6e7f2a317f8d783256b9c9")
    version("2.0.9", sha256="a0922e42f2d258505678e2f4a355c5476c1a6352c3f3a37754042ddb7e7cf72f")
    version("1.4.2", sha256="fda25ae5e99057f05bd339ea7972196d2f44e6fe8fb210951ab01f6609cdbdb7")
    version("1.2.1", sha256="d1afb253d6de230e73698377566da333ef42e1c82190216aa7a0c1b729d6ff4d")

    depends_on("py-setuptools", type="build")
    depends_on("py-future", type=("build", "run"), when="@:1")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"), when="@:1")
    depends_on("python@3.8:", type=("build", "run"), when="@2.0:")
    depends_on("gl", type=("build", "run"), when="@2.0: platform=linux")
    depends_on("pil", type=("build", "run"), when="@2.0: platform=linux")
    depends_on("pulseaudio", type=("build", "run"), when="@2.0: platform=linux")

    def url_for_version(self, version):
        if version <= Version("1.4.2"):
            return (
                f"https://files.pythonhosted.org/packages/source/p/pyglet/pyglet-{version}.tar.gz"
            )

    @when("@2.0.9:2.0.10")
    def patch(self):
        # 2.0.9 and 2.0.10 had a broken pyproject.toml in their PyPI zipfile
        if os.path.exists("pyproject.toml"):
            os.remove("pyproject.toml")
