# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySoyclustering(PythonPackage):
    """This package is implementation of Improving spherical k-means for document
    clustering. Fast initialization, sparse centroid projection, and efficient
    cluster labeling (Kim et al., 2020)."""

    homepage = "https://github.com/lovit/clustering4docs"
    pypi = "soyclustering/soyclustering-0.2.0.tar.gz"

    maintainers("meyersbs")

    version("0.2.0", sha256="fce7ed92671b26846114bfd893107d8fdbc8297bd035a5b8ad2999d066f1fb43")

    # From setup.py:
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.1:", type=("build", "run"))
    # From build errors:
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
