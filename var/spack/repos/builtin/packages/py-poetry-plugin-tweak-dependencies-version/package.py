# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetryPluginTweakDependenciesVersion(PythonPackage):
    """Poetry plugin used to tweak dependency versions."""

    homepage = "https://github.com/sbrunner/poetry-plugin-tweak-dependencies-version"
    pypi = "poetry_plugin_tweak_dependencies_version/"
    pypi += "poetry_plugin_tweak_dependencies_version-1.5.1.tar.gz"

    maintainers("LydDeb")

    version("1.5.1", sha256="4e0be2b8e23a04e542c5090deb5b6e191750ec45bace98ea8b55150844c6026b")

    depends_on("python@3.9:3.11", type=("build", "run"))
    depends_on("py-poetry-core@1.0.0:", type="build")
    depends_on("py-poetry-dynamic-versioning", type="build")
    depends_on("py-poetry@1.6", type=("build", "run"))
