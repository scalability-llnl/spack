# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyter(PythonPackage):
    """Jupyter metapackage. Install all the Jupyter components in one go."""

    homepage = "https://jupyter.org/"
    pypi = "jupyter/jupyter-1.0.0.tar.gz"

    license("BSD-3-Clause")

    version("1.1.1", sha256="d55467bceabdea49d7e3624af7e33d59c37fff53ed3a350e1ac957bed731de7a")
    version(
        "1.0.0",
        sha256="d9dc4b3318f310e34c82951ea5d6683f67bed7def4b259fafbfe4f1beb1d8e5f",
        deprecated=True,
    )

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-notebook")
        depends_on("py-qtconsole", when="@:1.0")
        depends_on("py-jupyter-console")
        depends_on("py-nbconvert")
        depends_on("py-ipykernel")
        depends_on("py-ipywidgets")
        depends_on("py-jupyterlab", when="@1.1:")
