# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeemap(PythonPackage):
    """A Python package for interactive mapping using Google Earth Engine and ipyleaflet."""

    homepage = "https://github.com/gee-community/geemap"
    pypi = "geemap/geemap-0.35.1.tar.gz"

    license("MIT")

    version("0.35.1", sha256="98f3f17fb1d07a6fe43b06f03fb680e10517adfd96002184015a3d4fe92435d6")

    with default_args(type="build"):
        depends_on("py-setuptools@64:")
        depends_on("py-setuptools-scm@8:")

    with default_args(type=("build", "run")):
        depends_on("py-bqplot")
        depends_on("py-colour")
        depends_on("py-earthengine-api@1:")
        depends_on("py-eerepr@0.0.4:")
        depends_on("py-folium@0.17:")
        depends_on("py-geocoder")
        depends_on("py-ipyevents")
        depends_on("py-ipyfilechooser@0.6:")
        depends_on("py-ipyleaflet@0.19.2:")
        depends_on("py-ipytree")
        depends_on("py-matplotlib")
        depends_on("py-numpy")
        depends_on("py-pandas")
        depends_on("py-plotly")
        depends_on("py-pyperclip")
        depends_on("py-pyshp@2.3.1:")
        depends_on("py-python-box")
        depends_on("py-scooby")
