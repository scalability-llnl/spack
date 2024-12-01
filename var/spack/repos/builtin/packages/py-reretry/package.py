# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReretry(PythonPackage):
    """Easy to use retry decorator."""

    homepage = "https://github.com/leshchenko1979/reretry"
    pypi = "reretry/reretry-0.11.8.tar.gz"
    maintainers("charmoniumQ")

    license("Apache-2.0")

    version("0.11.8", sha256="f2791fcebe512ea2f1d153a2874778523a8064860b591cd90afc21a8bed432e3")
    version("0.11.1", sha256="4ae1840ae9e443822bb70543c485bb9c45d1d009e32bd6809f2a9f2839149f5d")

    depends_on("python@3.7:", type=("build", "run"), when="@0.11.4:")
    depends_on("py-setuptools", type="build")
    depends_on("py-pbr", type="build", when="@:0.11.7")
