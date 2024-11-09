# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRiver(PythonPackage):
    """River is a Python library for online machine learning. It aims to be the most
    user-friendly library for doing machine learning on streaming data. River is the
    result of a merge between creme and scikit-multiflow."""

    homepage = "https://riverml.xyz/0.13.0/"
    pypi = "river/river-0.13.0.tar.gz"

    license("BSD-3-Clause")

    version("0.13.0", sha256="9d068b7a9db32302fbd581af81315681dfe61774a5d777fb3d5982d3c3061340")

    depends_on("c", type="build")  # generated

    # pyproject.toml
    depends_on("py-cython", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-rust", type="build")

    # setup.py
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy@1.22:", type=("build", "run"))
    depends_on("py-scipy@1.5:", type=("build", "run"))
    depends_on("py-pandas@1.3:", type=("build", "run"))
