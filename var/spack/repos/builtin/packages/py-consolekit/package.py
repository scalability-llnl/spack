# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyConsolekit(PythonPackage):
    """Additional utilities for click."""

    homepage = "https://github.com/domdfcoding/consolekit"
    pypi = "consolekit/consolekit-1.5.1.tar.gz"

    license("MIT")

    version("1.5.1", sha256="55ea43e226863e1d618ec9b860c9842d84249d895c3376c03b158d8f3a335626")

    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("py-click@7.1.2:", type=("build", "run"))
    depends_on("py-colorama@0.4.3:", type=("build", "run"), when="^python@:3.9 platform=windows")
    depends_on("py-deprecation-alias@0.1.1:", type=("build", "run"))
    depends_on("py-domdf-python-tools@2.6:", type=("build", "run"))
    depends_on("py-mistletoe@0.7.2:", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", type=("build", "run"))
    conflicts("^py-typing-extensions@3.10.0.1")
