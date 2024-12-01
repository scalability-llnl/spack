# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQtconsole(PythonPackage):
    """Jupyter Qt console"""

    homepage = "https://ipython.org"
    pypi = "qtconsole/qtconsole-4.2.1.tar.gz"

    license("BSD-3-Clause")

    version("5.2.0", sha256="6bb4df839609f240194213407872076f871e3a3884cf8e785068e8c7f39344c6")
    version("4.5.1", sha256="4af84facdd6f00a6b9b2927255f717bb23ae4b7a20ba1d9ef0a5a5a8dbe01ae2")
    version("4.2.1", sha256="25ec7d345528b3e8f3c91be349dd3c699755f206dc4b6ec668e2e5dd60ea18ef")

    variant("docs", default=False, description="Build documentation")

    depends_on("python@2.7:2.8,3.3:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@5.2.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-ipykernel@4.1:", type=("build", "run"))
    depends_on("py-jupyter-client@4.1:", type=("build", "run"))
    depends_on("py-jupyter-core", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-traitlets", type=("build", "run"))
    depends_on("py-ipython-genutils", type=("build", "run"), when="@4.5.1:")
    depends_on("py-sphinx@1.3:", type=("build", "run"), when="+docs")
    depends_on("py-pyqt5", type="run", when="@:5.1")
    depends_on("py-qtpy", type=("build", "run"), when="@5.2.0:")
    depends_on("py-pyzmq@17.1:", type=("build", "run"), when="@5.2.0:")
