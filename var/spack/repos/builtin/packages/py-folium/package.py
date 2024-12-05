# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFolium(PythonPackage):
    """Make beautiful maps with Leaflet.js & Python."""

    homepage = "https://python-visualization.github.io/folium"
    pypi = "folium/folium-0.16.0.tar.gz"

    license("MIT")

    version("0.16.0", sha256="2585ee9253dc758d3a365534caa6fb5fa0c244646db4dc5819afc67bbd4daabb")

    depends_on("py-setuptools@41.2:", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-branca@0.6.0:", type=("build", "run"))
    depends_on("py-jinja2@2.9:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-xyzservices", type=("build", "run"))
