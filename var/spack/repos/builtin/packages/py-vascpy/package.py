# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVascpy(PythonPackage):
    """Python library for reading, writing, and manipulating large-scale vasculature
    datasets"""

    homepage = "https://github.com/BlueBrain/vascpy"
    git = "https://github.com/BlueBrain/vascpy.git"
    pypi = "vascpy/vascpy-0.1.0.tar.gz"

    license("Apache-2.0")

    maintainers("tristan0x")

    version("main", branch="main")
    version("0.1.1", sha256="1b6bd1399a0388b36241364de74ef709cda2b659e45448fbbdd7efc93bbd8b27")

    depends_on("py-setuptools-scm@3.4:", type="build")
    depends_on("py-setuptools@42:", type="build")

    depends_on("py-click@8.0.0:", type=("build", "run"))
    depends_on("py-h5py@3.4.0:", type=("build", "run"))
    depends_on("py-libsonata@0.1.8:", type=("build", "run"))
    depends_on("py-morphio@3.0.0:", type=("build", "run"))
    depends_on("py-numpy@1.17.0:", type=("build", "run"))
    depends_on("py-pandas@1.0.0:", type=("build", "run"))
    depends_on("py-scipy@1.0.0:", type=("build", "run"))
