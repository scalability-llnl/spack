# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMplhep(PythonPackage):
    """Matplotlib styles for HEP"""

    homepage = "https://github.com/scikit-hep/mplhep"
    pypi = "mplhep/mplhep-0.3.15.tar.gz"

    license("MIT")

    version("0.3.26", sha256="d707a95ce59b0bac2fe4fe1c57fede14e15da639f3a7c732e7513a753fd9e9ac")
    version("0.3.15", sha256="595f796ea65930094e86a805214e0d44537ead267a7487ae16eda02d1670653e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@39.2:", type="build")
    depends_on("py-setuptools@42:", when="@0.3.26:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", when="@0.3.2:", type="build")
    depends_on("py-matplotlib@3.4:", type=("build", "run"))
    depends_on("py-mplhep-data", type=("build", "run"))
    depends_on("py-numpy@1.16.0:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-uhi@0.2.0:", type=("build", "run"))
