# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyShellingham(PythonPackage):
    """Tool to Detect Surrounding Shell"""

    homepage = "https://github.com/sarugaku/shellingham"
    pypi = "shellingham/shellingham-1.4.0.tar.gz"

    license("0BSD")

    version("1.5.0", sha256="72fb7f5c63103ca2cb91b23dee0c71fe8ad6fbfd46418ef17dbe40db51592dad")
    version("1.4.0", sha256="4855c2458d6904829bd34c299f11fdeed7cfefbf8a2c522e4caea6cd76b3171e")

    depends_on("python@2.6:2.7,3.4:", type=("build", "run"))
    depends_on("python@3.4:", when="@1.5.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
