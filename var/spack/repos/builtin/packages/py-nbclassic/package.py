# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbclassic(PythonPackage):
    """Jupyter Notebook as a Jupyter Server Extension."""

    homepage = "https://github.com/jupyterlab/nbclassic"
    pypi = "nbclassic/nbclassic-0.3.1.tar.gz"

    license("BSD-3-Clause")

    version("1.0.0", sha256="0ae11eb2319455d805596bf320336cda9554b41d99ab9a3c31bf8180bffa30e3")
    version("0.4.8", sha256="c74d8a500f8e058d46b576a41e5bc640711e1032cf7541dde5f73ea49497e283")
    version("0.3.5", sha256="99444dd63103af23c788d9b5172992f12caf8c3098dd5a35c787f0df31490c29")
    version("0.3.1", sha256="f920f8d09849bea7950e1017ff3bd101763a8d68f565a51ce053572e65aa7947")

    depends_on("py-setuptools", type="build")
    depends_on("py-jupyter-packaging@0.9:0", when="@0.3.3:", type="build")
    depends_on("py-babel", when="@0.4:", type="build")

    depends_on("py-jinja2", when="@0.4:", type=("build", "run"))
    depends_on("py-tornado@6.1:", when="@0.4:", type=("build", "run"))
    depends_on("py-pyzmq@17:", when="@0.4:", type=("build", "run"))
    depends_on("py-argon2-cffi", when="@0.4:", type=("build", "run"))
    depends_on("py-traitlets@4.2.1:", when="@0.4:", type=("build", "run"))
    depends_on("py-jupyter-core@4.6.1:", when="@0.4:", type=("build", "run"))
    depends_on("py-jupyter-client@6.1.1:", when="@0.4:", type=("build", "run"))
    depends_on("py-ipython-genutils", when="@0.4:", type=("build", "run"))
    # version requirement for py-jupyter-server comes from pyproject.toml
    depends_on("py-jupyter-server@1.17:", when="@0.4:", type=("build", "run"))
    depends_on("py-jupyter-server@1.8:", when="@0.3.7", type=("build", "run"))
    depends_on("py-jupyter-server@1.8:1", when="@:0.3.6", type=("build", "run"))
    depends_on("py-nbformat", when="@0.4:", type=("build", "run"))
    depends_on("py-notebook-shim@0.2.3:", when="@0.5.6:", type=("build", "run"))
    depends_on("py-notebook-shim@0.1:", when="@0.3.6:", type=("build", "run"))
    depends_on("py-nbconvert@5:", when="@0.4:", type=("build", "run"))
    depends_on("py-nest-asyncio@1.5:", when="@0.4:", type=("build", "run"))
    depends_on("py-ipykernel", when="@0.4:", type=("build", "run"))
    depends_on("py-send2trash@1.8:", when="@0.4:", type=("build", "run"))
    depends_on("py-terminado@0.8.3:", when="@0.4:", type=("build", "run"))
    depends_on("py-prometheus-client", when="@0.4:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-notebook@:6", when="@:0.3.7", type=("build", "run"))
