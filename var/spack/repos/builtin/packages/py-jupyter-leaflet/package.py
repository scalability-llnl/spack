# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterLeaflet(PythonPackage):
    """ipyleaflet extensions for JupyterLab and Jupyter Notebook."""

    homepage = "https://github.com/jupyter-widgets/ipyleaflet"
    pypi = "jupyter_leaflet/jupyter_leaflet-0.19.2.tar.gz"

    license("MIT")

    version("0.19.2", sha256="b09b5ba48b1488cb61da37a6f558347269eb53ff6d64dc1a73e005ffc4420063")

    with default_args(type="build"):
        depends_on("py-hatchling")
        depends_on("py-jupyterlab@4")
        depends_on("py-hatch-nodejs-version@0.3.2:")
        depends_on("py-hatch-jupyter-builder@0.8.1:")
