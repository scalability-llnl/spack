# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKmodes(PythonPackage):
    """Python implementations of the k-modes and k-prototypes clustering
    algorithms for clustering categorical data."""

    homepage = "https://github.com/nicodv/kmodes"
    pypi = "kmodes/kmodes-0.10.1.tar.gz"

    license("MIT")

    version("0.10.1", sha256="3222c2f672a6356be353955c02d1e38472d9f6074744b4ffb0c058e8c2235ea1")

    depends_on("python@3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.10.4:", type=("build", "run"))
    depends_on("py-scikit-learn@0.19.0:", type=("build", "run"))
    depends_on("py-scipy@0.13.3:", type=("build", "run"))
    depends_on("py-joblib@0.11:", type=("build", "run"))
