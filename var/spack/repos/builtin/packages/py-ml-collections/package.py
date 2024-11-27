# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMlCollections(PythonPackage):
    """ML Collections is a library of Python collections designed for ML usecases."""

    homepage = "https://https://github.com/google/ml_collections"
    pypi = "ml_collections/ml_collections-0.1.0.tar.gz"
    git = "https://github.com/google/ml_collections"

    license("Apache-2.0")

    version("0.1.1", sha256="3fefcc72ec433aa1e5d32307a3e474bbb67f405be814ea52a2166bfc9dbe68cc")
    version("0.1.0", commit="63a7c22d1bf3521c3bb3f9da6ebf07972c25fec4")

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-absl-py", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-contextlib2", type=("build", "run"))
