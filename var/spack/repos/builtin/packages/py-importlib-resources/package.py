# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImportlibResources(PythonPackage):
    """Read resources from Python packages"""

    homepage = "https://github.com/python/importlib_resources"
    pypi = "importlib_resources/importlib_resources-1.0.2.tar.gz"

    license("Apache-2.0")

    version("5.12.0", sha256="4be82589bf5c1d7999aedf2a45159d10cb3ca4f19b2271f8792bc8e6da7b22f6")
    version("5.9.0", sha256="5481e97fb45af8dcf2f798952625591c58fe599d0735d86b10f54de086a61681")
    version("5.3.0", sha256="f2e58e721b505a79abe67f5868d99f8886aec8594c962c7490d0c22925f518da")
    version("5.2.3", sha256="203d70dda34cfbfbb42324a8d4211196e7d3e858de21a5eb68c6d1cdd99e4e98")
    version("5.2.2", sha256="a65882a4d0fe5fbf702273456ba2ce74fe44892c25e42e057aca526b702a6d4b")
    version("5.1.0", sha256="bfdad047bce441405a49cf8eb48ddce5e56c696e185f59147a8b79e75e9e6380")
    version("1.0.2", sha256="d3279fd0f6f847cced9f7acc19bd3e5df54d34f93a2e7bb5f238f81545787078")

    depends_on("py-setuptools@56:", when="@5.9.0:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@3.4.1:+toml", when="@5:", type="build")

    depends_on("py-zipp@3.1.0:", when="@5.2.2: ^python@:3.9", type=("build", "run"))
    depends_on("py-zipp@0.4:", when="@5.0:5.1", type=("build", "run"))
