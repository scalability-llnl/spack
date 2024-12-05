# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyevents(PythonPackage):
    """A custom widget for returning mouse and keyboard events to Python."""

    homepage = "https://github.com/mwcraig/ipyevents"
    pypi = "ipyevents/ipyevents-2.0.1.tar.gz"

    license("BSD-3-Clause")

    version("2.0.1", sha256="23eb2afab13d9056397f120a88051dd3beb067b698d08b33adffc9e077f019cb")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@40.8:", type="build")
    depends_on("py-jupyter-packaging@0.7", type="build")
    depends_on("py-jupyterlab@3.0:3", type="build")
    depends_on("py-ipywidgets@7.6:", type=("build", "run"))
