# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpycanvas(PythonPackage):
    """Interactive Canvas in Jupyter."""

    homepage = "https://github.com/martinRenou/ipycanvas"
    pypi = "ipycanvas/ipycanvas-0.9.0.tar.gz"

    license("BSD-3-Clause")

    version("0.10.2", sha256="a02c494834cb3c60509801172e7429beae837b3cb6c61d3becf8b586c5a66004")
    version("0.9.0", sha256="f29e56b93fe765ceace0676c3e75d44e02a3ff6c806f3b7e5b869279f470cc43")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@40.8:", type="build")
    depends_on("py-jupyter-packaging@0.7", type="build")
    depends_on("py-jupyterlab@3.0:3", type="build")
    depends_on("py-ipywidgets@7.6:", type=("build", "run"))
    depends_on("pil@6:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
