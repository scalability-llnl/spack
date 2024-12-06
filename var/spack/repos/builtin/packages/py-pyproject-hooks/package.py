# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprojectHooks(PythonPackage):
    """Wrappers to call pyproject.toml-based build backend hooks."""

    homepage = "https://github.com/pypa/pyproject-hooks"
    pypi = "pyproject_hooks/pyproject_hooks-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="f271b298b97f5955d53fb12b72c1fb1948c22c1a6b70b315c54cedaca0264ef5")

    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))
