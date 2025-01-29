# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBqplot(PythonPackage):
    """Interactive plotting for the Jupyter notebook, using d3.js and ipywidgets."""

    homepage = "https://github.com/bqplot/bqplot"
    # Source code only available on GitHub, has build issues
    url = "https://files.pythonhosted.org/packages/py2.py3/b/bqplot/bqplot-0.12.44-py2.py3-none-any.whl"

    license("Apache-2.0")

    version("0.12.44", sha256="cad65bf5c4ce7ea7b03e1c674340f9274c0975941e63057831b29f7c2c37f144")

    with default_args(type=("build", "run")):
        depends_on("py-ipywidgets@7.5:8")
        depends_on("py-traitlets@4.3:")
        depends_on("py-traittypes@0.0.6:")
        depends_on("py-numpy@1.10.4:")
        depends_on("py-pandas@1:2")
