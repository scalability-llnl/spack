# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpympl(PythonPackage):
    """Matplotlib Jupyter Extension."""

    homepage = "https://github.com/matplotlib/ipympl"
    pypi = "ipympl/ipympl-0.8.8.tar.gz"
    maintainers("haralmha")

    license("BSD-3-Clause")

    version("0.9.4", sha256="cfb53c5b4fcbcee6d18f095eecfc6c6c474303d5b744e72cc66e7a2804708907")
    # Build failures
    version(
        "0.8.8",
        sha256="5bf5d780b07fafe7924922ac6b2f3abd22721f341e5e196b3b82737dfbd0e1c9",
        deprecated=True,
    )

    with default_args(type="build"):
        with when("@0.9:"):
            depends_on("py-hatchling")
            depends_on("py-jupyterlab@4")
            depends_on("py-hatch-nodejs-version@0.3.2:")

        # Historical dependencies
        with when("@:0.8"):
            depends_on("py-jupyter-packaging@0.7")
            depends_on("py-jupyterlab@3")
            depends_on("py-setuptools@40.8:")
            depends_on("yarn")

    with default_args(type=("build", "run")):
        depends_on("py-ipython@:8")
        depends_on("py-ipython-genutils")
        depends_on("py-ipywidgets@7.6:8", when="@0.9:")
        depends_on("py-ipywidgets@7.6:7", when="@:0.8")
        depends_on("py-matplotlib@3.4:3", when="@0.9:")
        depends_on("py-matplotlib@2:3", when="@:0.8")
        depends_on("py-numpy")
        depends_on("pil")
        depends_on("py-traitlets@:5")

        # Necessary for jupyter extension env vars
        depends_on("py-jupyter-core")
