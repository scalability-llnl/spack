# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydocstyle(PythonPackage):
    """Python docstring style checker."""

    homepage = "https://github.com/PyCQA/pydocstyle/"
    pypi = "pydocstyle/pydocstyle-6.1.1.tar.gz"

    maintainers("adamjstewart")

    license("MIT")

    version("6.2.1", sha256="5ddccabe3c9555d4afaabdba909ca2de4fa24ac31e2eede4ab3d528a4bcadd52")
    version("6.2.0", sha256="b2d280501a4c0d9feeb96e9171dc3f6f7d0064c55270f4c7b1baa18452019fd9")
    version("6.1.1", sha256="1d41b7c459ba0ee6c345f2eb9ae827cab14a7533a88c5c6f7e94923f72df92dc")

    variant("toml", default=True, description="Allow pydocstyle to read pyproject.toml")

    depends_on("py-poetry-core", when="@6.2:", type="build")
    depends_on("py-setuptools", when="@:6.1", type="build")
    depends_on("py-snowballstemmer@2.2:", when="@6.2:", type=("build", "run"))
    depends_on("py-snowballstemmer", type=("build", "run"))
    depends_on("py-tomli@1.2.3:", when="@6.2.1:+toml ^python@:3.10", type=("build", "run"))
    depends_on("py-toml@0.10.2:", when="@6.2.0+toml", type=("build", "run"))
    depends_on("py-toml", when="@:6.1+toml", type=("build", "run"))
    depends_on("py-importlib-metadata@2:4", when="@6.2: ^python@:3.7", type=("build", "run"))
