# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqtgraph(PythonPackage):
    """PyQtGraph is a pure-python graphics and GUI library intended for use in mathematics,
    scientific, and engineering applications"""

    homepage = "https://www.pyqtgraph.org/"
    pypi = "pyqtgraph/pyqtgraph-0.13.3.tar.gz"

    license("MIT", checked_by="A-N-Other")

    version("0.13.7", sha256="64f84f1935c6996d0e09b1ee66fe478a7771e3ca6f3aaa05f00f6e068321d9e3")
    version("0.13.3", sha256="58108d8411c7054e0841d8b791ee85e101fc296b9b359c0e01dde38a98ff2ace")

    depends_on("python@3.8:", when="@:0.13.3", type=("build", "run"))
    depends_on("python@3.9:", when="@0.13.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.20:", when="@:0.13.3", type=("build", "run"))
    depends_on("py-numpy@1.22:", when="@0.13.4:", type=("build", "run"))

    # currently there are no packages for all variants...
    apis = ["pyqt6", "pyqt5", "pyside2"]  # pyside6

    variant("api", default="pyqt6", description="Default QT API", values=apis, multi=False)

    for api in apis:
        depends_on("py-" + api, when="api=" + api, type=("build", "run"))

    # todo: optional dependencies, see https://github.com/pyqtgraph/pyqtgraph?tab=readme-ov-file#optional-added-functionalities

    # see https://github.com/pyqtgraph/pyqtgraph/blob/44745a7ba5f8251b2f815f3188b80d579e9f93af/pyqtgraph/Qt/__init__.py#L25
    def setup_run_environment(self, env):
        api = self.spec.variants["api"].value
        if api == "pyqt6":
            env.set("PYQTGRAPH_QT_LIB", "PyQt6")
        elif api == "pyside6":
            env.set("PYQTGRAPH_QT_LIB", "PySide6")
        elif api == "pyqt5":
            env.set("PYQTGRAPH_QT_LIB", "PyQt5")
        elif api == "pyside2":
            env.set("PYQTGRAPH_QT_LIB", "PySide2")
