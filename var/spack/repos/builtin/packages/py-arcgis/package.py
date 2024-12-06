# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArcgis(PythonPackage):
    """ArcGIS API for Python."""

    homepage = "https://developers.arcgis.com/python/"
    pypi = "arcgis/arcgis-1.8.4.tar.gz"

    version("1.8.4", sha256="f1445dac25d3d4c03755d716c74a0930881c6be3cd36d22c6ff5ac754f9842d7")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-ipywidgets@7:", type=("build", "run"))
    depends_on("py-widgetsnbextension@3:", type=("build", "run"))
    depends_on("py-pandas@1:", type=("build", "run"))
    depends_on("py-numpy@1.16.2:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-keyring@19:", type=("build", "run"))
    depends_on("py-lerc", type=("build", "run"))
    depends_on("py-ujson@3:", type=("build", "run"))
    depends_on("py-jupyterlab", type=("build", "run"))
    depends_on("py-python-certifi-win32", type=("build", "run"))
    depends_on("py-pyshp@2:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-requests-oauthlib", type=("build", "run"))
    depends_on("py-requests-toolbelt", type=("build", "run"))
    depends_on("py-requests-ntlm", type=("build", "run"))

    def global_options(self, spec, prefix):
        return ["--conda-install-mode"]
