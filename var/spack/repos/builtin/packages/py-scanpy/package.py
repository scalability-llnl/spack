# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScanpy(PythonPackage):
    """Scanpy is a scalable toolkit for analyzing single-cell
    gene expression data built jointly with anndata."""

    homepage = "https://scanpy.readthedocs.io/en/stable/"
    pypi = "scanpy/scanpy-1.9.1.tar.gz"

    license("BSD-3-Clause")

    version("1.9.1", sha256="00c9a83b649da7e0171c91e9a08cff632102faa760614fd05cd4d1dbba4eb541")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-flit-core@3.4:3", type="build")
    depends_on("py-importlib-metadata@0.7:", type=("build", "run"), when="^python@:3.7")
    depends_on("py-tomli", type="build")
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-anndata@0.7.4:", type=("build", "run"))
    depends_on("py-numpy@1.17.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.4:", type=("build", "run"))
    depends_on("py-pandas@1.0:", type=("build", "run"))
    depends_on("py-scipy@1.4:", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-h5py@3:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-scikit-learn@0.22:", type=("build", "run"))
    depends_on("py-statsmodels@0.10.0:", type=("build", "run"))
    depends_on("py-patsy", type=("build", "run"))
    depends_on("py-networkx@2.3:", type=("build", "run"))
    depends_on("py-natsort", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-numba@0.41.0:", type=("build", "run"))
    depends_on("py-umap-learn@0.3.10:", type=("build", "run"))
    depends_on("py-session-info", type=("build", "run"))
