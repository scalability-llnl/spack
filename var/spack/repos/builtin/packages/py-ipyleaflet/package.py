# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyleaflet(PythonPackage):
    """A Jupyter widget for dynamic Leaflet maps."""

    homepage = "https://github.com/jupyter-widgets/ipyleaflet"
    pypi = "ipyleaflet/ipyleaflet-0.19.2.tar.gz"

    license("MIT")

    version("0.19.2", sha256="b3b83fe3460e742964c2a5924ea7934365a3749bb75310ce388d45fd751372d2")

    depends_on("py-hatchling", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-ipywidgets@7.6:8")
        depends_on("py-traittypes@0.2.1:2")
        depends_on("py-xyzservices@2021.8.1:")
        depends_on("py-branca@0.5:")
        depends_on("py-jupyter-leaflet@0.19")
