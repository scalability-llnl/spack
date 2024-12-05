# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySpatialist(PythonPackage):
    """This package offers functionalities for user-friendly geo data
    processing using GDAL and OGR."""

    homepage = "https://github.com/johntruckenbrodt/spatialist"
    pypi = "spatialist/spatialist-0.4.tar.gz"

    maintainers("adamjstewart")

    version("0.4", sha256="153b118022c06ad2d1d51fb6cd9ecbfc8020bc1995b643ec7fa689a8c5dde7e9")
    version("0.2.8", sha256="97de7f9c0fbf28497ef28970bdf8093a152e691a783e7edad22998cb235154c6")

    depends_on("python@2.7.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-progressbar2", type=("build", "run"))
    depends_on("py-jupyter", type=("build", "run"))
    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-ipywidgets", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-prompt-toolkit@2.0.10:2.0", type=("build", "run"))
    depends_on("py-pathos@0.2:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scoop", type=("build", "run"))
    depends_on("py-tblib", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
