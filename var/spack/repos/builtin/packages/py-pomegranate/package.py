# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPomegranate(PythonPackage):
    """Fast, flexible and easy to use probabilistic modelling in Python."""

    homepage = "https://github.com/jmschrei/pomegranate"
    pypi = "pomegranate/pomegranate-0.12.0.tar.gz"

    license("MIT")

    version("0.12.0", sha256="8b00c88f7cf9cad8d38ea00ea5274821376fefb217a1128afe6b1fcac54c975a")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.22.1:", type="build")
    depends_on("py-numpy@1.8.0:", type=("build", "run"))
    depends_on("py-joblib@0.9.0b4:", type=("build", "run"))
    depends_on("py-networkx@2.0:", type=("build", "run"))
    depends_on("py-scipy@0.17.0:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
