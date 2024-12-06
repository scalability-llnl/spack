# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNglview(PythonPackage):
    """Jupyter widget to interactively view molecular structures and trajectories."""

    homepage = "http://nglviewer.org"
    pypi = "nglview/nglview-3.0.8.tar.gz"

    maintainers("w8jcik")

    version("3.0.8", sha256="f9e468cd813dac319cbeca6ae20ae099008ff3a06399f5d23d75582dde28623a")

    depends_on("py-ipywidgets@7:", type=("build", "run"))
    depends_on("py-jupyterlab-widgets", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-setuptools@40.8.0:", type="build")
    depends_on("py-jupyter-packaging@0.7.9:0.7", type="build")
    depends_on("py-versioneer-518", type="build")
