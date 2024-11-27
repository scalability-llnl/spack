# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyflakes(PythonPackage):
    """A simple program which checks Python source files for errors."""

    homepage = "https://github.com/PyCQA/pyflakes"
    pypi = "pyflakes/pyflakes-2.4.0.tar.gz"

    license("MIT")

    version("3.1.0", sha256="a0aae034c444db0071aa077972ba4768d40c830d9539fd45bf4cd3f8f6992efc")
    version("3.0.1", sha256="ec8b276a6b60bd80defed25add7e439881c19e64850afd9b346283d4165fd0fd")
    version("2.5.0", sha256="491feb020dca48ccc562a8c0cbe8df07ee13078df59813b83959cbdada312ea3")
    version("2.4.0", sha256="05a85c2872edf37a4ed30b0cce2f6093e1d0581f8c19d7393122da7e25b2b24c")
    version("2.3.0", sha256="e59fd8e750e588358f1b8885e5a4751203a0516e0ee6d34811089ac294c8806f")
    version("2.2.0", sha256="35b2d75ee967ea93b55750aa9edbbf72813e06a66ba54438df2cfac9e3c27fc8")
    version("2.1.1", sha256="d976835886f8c5b31d47970ed689944a0262b5f3afa00a5a7b4dc81e5449f8a2")
    version("2.1.0", sha256="5e8c00e30c464c99e0b501dc160b13a14af7f27d4dffb529c556e30a159e231d")
    version("1.6.0", sha256="8d616a382f243dbf19b54743f280b80198be0bca3a5396f1d2e1fca6223e8805")
    version("1.5.0", sha256="aa0d4dff45c0cc2214ba158d29280f8fa1129f3e87858ef825930845146337f4")
    version("1.4.0", sha256="05c8a1702088e9b54acb422f78210afc6074b3472afa7a0a77f0b8aa3f5db605")
    version("1.3.0", sha256="a4f93317c97a9d9ed71d6ecfe08b68e3de9fea3f4d94dcd1d9d83ccbf929bc31")
    version("1.2.3", sha256="2e4a1b636d8809d8f0a69f341acf15b2e401a3221ede11be439911d23ce2139e")
    version("1.2.2", sha256="58741f9d3bffeba8f88452c1eddcf1b3eee464560e4589e4b81de8b3c9e42e4d")
    version("1.2.1", sha256="7e5e3a5e7ce8d1afb9cbcff2bb10cffaf83e1d94ab7c78eb86a715a88c32e22f")
    version("1.2.0", sha256="3633e000ffdc307ff1a7d7450e895ff8813e20b084ef263b5669eef9bc4c7a52")
    version("1.1.0", sha256="e5f959931987e2be178781554b485d52342ec9f1b43f891d2dad07a691c7a89a")
    version("0.9.2", sha256="02691c23ce699f252874b7c27f14cf26e3d4e82b58e5d584f000b7ab5be36a5f")
    version("0.9.1", sha256="baad29ac1e884c7077eb32ed1d9ee5cf30bf4b888329e1fcb51b9aa5298cb3b9")
    version("0.9.0", sha256="4c4d73085ce5de9d8147011c060d129659baa1111d1a5a3035f2bd03f2976538")

    depends_on("python@3.6:", when="@2.5:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pyflakes requires py-setuptools during runtime as well.
    depends_on("py-setuptools", type=("build", "run"))
