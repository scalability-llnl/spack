# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsEntryPointsSelectable(PythonPackage):
    """Compatibility shim providing selectable entry points for older implementations"""

    homepage = "https://github.com/jaraco/backports.entry_points_selectable"
    pypi = "backports.entry_points_selectable/backports.entry_points_selectable-1.1.0.tar.gz"

    license("MIT")

    version("1.1.1", sha256="914b21a479fde881635f7af5adc7f6e38d6b274be32269070c53b698c60d5386")
    version("1.1.0", sha256="988468260ec1c196dab6ae1149260e2f5472c9110334e5d51adcb77867361f6a")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools@56:", when="@1.1.1: ^python@3.6:", type="build")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm+toml@3.4.1:", type="build")

    depends_on("py-importlib-metadata", when="^python@:3.7", type=("build", "run"))
