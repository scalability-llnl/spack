# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDomdfPythonTools(PythonPackage):
    """Helpful functions for Python"""

    homepage = "https://github.com/domdfcoding/domdf_python_tools"
    pypi = "domdf_python_tools/domdf_python_tools-3.6.1.tar.gz"

    license("MIT")

    version("3.6.1", sha256="acc04563d23bce4d437dd08af6b9bea788328c412772a044d8ca428a7ad861be")

    depends_on("py-wheel@0.34.2:", type="build")
    depends_on("py-setuptools@40.6:", type="build")
    conflicts("^py-setuptools@61")
    depends_on("py-importlib-metadata@3.6:", type=("build", "run"), when="^python@:3.8")
    depends_on("py-natsort@7.0.1:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.1:", type=("build", "run"))
