# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUmapLearn(PythonPackage):
    """Uniform Manifold Approximation and Projection (UMAP) is a dimension
    reduction technique that can be used for visualisation similarly to t-SNE,
    but also for general non-linear dimension reduction."""

    homepage = "https://github.com/lmcinnes/umap"
    pypi = "umap-learn/umap-learn-0.5.3.tar.gz"

    license("BSD-3-Clause")

    version("0.5.3", sha256="dbd57cb181c2b66d238acb5635697526bf24c798082daed0cf9b87f6a3a6c0c7")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-scikit-learn@0.22:", type=("build", "run"))
    depends_on("py-scipy@1.0:", type=("build", "run"))
    depends_on("py-numba@0.49:", type=("build", "run"))
    depends_on("py-pynndescent@0.5:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
