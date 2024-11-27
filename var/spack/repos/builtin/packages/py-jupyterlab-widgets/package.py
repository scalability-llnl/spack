# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterlabWidgets(PythonPackage):
    """A JupyterLab extension."""

    homepage = "https://github.com/jupyter-widgets/ipywidgets"
    # Source is also available, but I'm having issues getting it to build:
    # https://github.com/jupyter-widgets/ipywidgets/issues/3324
    url = "https://files.pythonhosted.org/packages/py3/j/jupyterlab_widgets/jupyterlab_widgets-1.0.2-py3-none-any.whl"

    license("BSD-3-Clause")

    version("3.0.3", sha256="6aa1bc0045470d54d76b9c0b7609a8f8f0087573bae25700a370c11f82cb38c8")
    version("1.1.0", sha256="c2a9bd3789f120f64d73268c066ed3b000c56bc1dda217be5cdc43e7b4ebad3f")
    version("1.0.2", sha256="f5d9efface8ec62941173ba1cffb2edd0ecddc801c11ae2931e30b50492eb8f7")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("python@3.7:", when="@3.0.3:", type=("build", "run"))
