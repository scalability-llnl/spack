# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyevents(PythonPackage):
    """A custom widget for returning mouse and keyboard events to Python."""

    homepage = "https://github.com/mwcraig/ipyevents"
    pypi = "ipyevents/ipyevents-2.0.1.tar.gz"

    license("BSD-3-Clause")

    version("2.0.2", sha256="26e878b0c5854bc8b6bd6a2bd2c89b314ebe86fda642f4d2434051545bab258f")
    version(
        "2.0.1",
        sha256="23eb2afab13d9056397f120a88051dd3beb067b698d08b33adffc9e077f019cb",
        deprecated=True,
    )

    with default_args(type="build"):
        depends_on("py-hatchling", when="@2.0.2:")
        depends_on("py-jupyterlab@3")
        depends_on("py-hatch-jupyter-builder@0.8.3:", when="@2.0.2:")

        # Historical dependencies
        depends_on("py-setuptools@40.8:", when="@:2.0.1")
        depends_on("py-jupyter-packaging@0.7", when="@:2.0.1")

    depends_on("py-ipywidgets@7.6:", type=("build", "run"))
