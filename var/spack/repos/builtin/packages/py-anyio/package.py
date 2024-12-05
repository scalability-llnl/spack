# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnyio(PythonPackage):
    """High level compatibility layer for multiple asynchronous event loop
    implementations."""

    homepage = "https://github.com/agronholm/anyio"
    pypi = "anyio/anyio-3.2.1.tar.gz"

    license("MIT")

    version("4.0.0", sha256="f7ed51751b2c2add651e5747c891b47e26d2a21be5d32d9311dfe9692f3e5d7a")
    version("3.6.2", sha256="25ea0d673ae30af41a0c442f81cf3b38c7e79fdc7b60335a4c14e05eb0947421")
    version("3.6.1", sha256="413adf95f93886e442aea925f3ee43baa5a765a64a0f52c6081894f9992fdd0b")
    version("3.5.0", sha256="a0aeffe2fb1fdf374a8e4b471444f0f3ac4fb9f5a5b542b48824475e0042a5a6")
    version("3.3.4", sha256="67da67b5b21f96b9d3d65daa6ea99f5d5282cb09f50eb4456f8fb51dffefc3ff")
    version("3.2.1", sha256="07968db9fa7c1ca5435a133dc62f988d84ef78e1d9b22814a59d1c62618afbc5")

    depends_on("python@3.8:", when="@4:", type=("build", "run"))
    depends_on("python@3.6.2:", type=("build", "run"))
    depends_on("py-setuptools@64:", when="@3.7:", type="build")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@6.4:", when="@3.7:", type="build")
    depends_on("py-setuptools-scm+toml@3.4:", when="@:3.6", type="build")

    depends_on("py-exceptiongroup@1.0.2:", when="@4: ^python@:3.10", type=("build", "run"))
    depends_on("py-idna@2.8:", type=("build", "run"))
    depends_on("py-sniffio@1.1:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-wheel@0.29:", when="@:3.6", type="build")
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
