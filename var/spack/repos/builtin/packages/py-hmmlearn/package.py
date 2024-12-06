# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHmmlearn(PythonPackage):
    """hmmlearn is a set of algorithms for unsupervised learning and
    inference of Hidden Markov Models."""

    homepage = "https://github.com/hmmlearn/hmmlearn"
    pypi = "hmmlearn/hmmlearn-0.3.0.tar.gz"

    maintainers("snehring")

    license("BSD-3-Clause")

    version("0.3.0", sha256="d13a91ea3695df881465e3d36132d7eef4e84d483f4ba538a4b46e24b5ea100f")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@3.3:", type="build")
    depends_on("py-pybind11@2.6:", type="build")

    depends_on("py-numpy@1.10:", type=("build", "run"))
    depends_on("py-scikit-learn@0.16:", type=("build", "run"))
    depends_on("py-scipy@0.19:", type=("build", "run"))

    conflicts("py-scikit-learn@=0.22.0", msg="Not compatible with scikit-learn@0.22.0")
