# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQtpy(PythonPackage):
    """QtPy: Abtraction layer for PyQt5/PyQt4/PySide/PySide2"""

    homepage = "https://github.com/spyder-ide/qtpy"
    pypi = "QtPy/QtPy-1.2.1.tar.gz"

    license("MIT")

    version("1.11.2", sha256="d6e4ae3a41f1fcb19762b58f35ad6dd443b4bdc867a4cb81ef10ccd85403c92b")
    version("1.7.1", sha256="e97275750934b3a1f4d8e263f5b889ae817ed36f26867ab0ce52be731ab1ed9e")
    version("1.2.1", sha256="5803ce31f50b24295e8e600b76cc91d7f2a3140a5a0d526d40226f9ec5e9097d")

    apis = ["pyqt5", "pyqt4", "pyside2", "pyside"]

    variant("api", default="pyqt5", description="Default QT API", values=apis, multi=False)

    depends_on("python@2.7:2.8,3.6:", when="@1.10.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    for api in apis:
        depends_on("py-" + api, when="api=" + api, type="run")

    def setup_run_environment(self, env):
        env.set("QT_API", self.spec.variants["api"].value)
