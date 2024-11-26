# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupyterlabPygments(PythonPackage):
    """Pygments theme using JupyterLab CSS variables."""

    homepage = "https://jupyter.org/"
    url = "https://files.pythonhosted.org/packages/py2.py3/j/jupyterlab-pygments/jupyterlab_pygments-0.2.2-py2.py3-none-any.whl"
    # We use wheels because in @0.2.2: there is a cyclic dependency between
    # py-nbconvert and py-jupyter-server:
    # py-nbconvert -> py-jupyterlab-pygments -> py-jupyterlab ->
    # -> py-jupyter-server -> py-nbconvert
    # Reported here: https://github.com/jupyterlab/jupyterlab_pygments/issues/23

    version("0.2.2", sha256="2405800db07c9f770863bcf8049a529c3dd4d3e28536638bd7c1c01d2748309f")
    version("0.1.2", sha256="abfb880fd1561987efaefcb2d2ac75145d2a5d0139b1876d5be806e32f630008")
    version("0.1.1", sha256="c9535e5999f29bff90bd0fa423717dcaf247b71fad505d66b17d3217e9021fc5")

    depends_on("python@3.7:", when="@0.2.2:", type=("build", "run"))
    depends_on("py-pygments@2.4.1:2", type=("build", "run"))
