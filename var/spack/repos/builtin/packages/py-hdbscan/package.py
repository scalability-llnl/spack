# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyHdbscan(PythonPackage):
    """HDBSCAN - Hierarchical Density-Based Spatial Clustering of
    Applications with Noise. Performs DBSCAN over varying epsilon
    values and integrates the result to find a clustering that gives
    the best stability over epsilon. This allows HDBSCAN to find
    clusters of varying densities (unlike DBSCAN), and be more robust
    to parameter selection. In practice this means that HDBSCAN
    returns a good clustering straight away with little or no
    parameter tuning -- and the primary parameter, minimum cluster
    size, is intuitive and easy to select.  HDBSCAN is ideal for
    exploratory data analysis; it's a fast and robust algorithm that
    you can trust to return meaningful clusters (if there are any)."""

    homepage = "https://github.com/scikit-learn-contrib/hdbscan"
    url = "https://github.com/scikit-learn-contrib/hdbscan/archive/0.8.26.tar.gz"

    license("BSD-3-Clause")

    version("0.8.29", sha256="67ba1c00b5ad7c0dca2d662d6036b6df235bd61522a785d68a8458b732555d76")
    version("0.8.26", sha256="2fd10906603b6565ee138656b6d59df3494c03c5e8099aede400d50b13af912b")

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.27:", type=("build", "run"))
    depends_on("py-numpy@1.16.0:", type=("build", "run"))
    depends_on("py-numpy@1.20:", type=("build", "run"), when="@0.8.29:")
    depends_on("py-scipy@0.9:", type=("build", "run"))
    depends_on("py-scipy@1.0:", type=("build", "run"), when="@0.8.29:")
    depends_on("py-scikit-learn@0.17:", type=("build", "run"))
    depends_on("py-scikit-learn@0.20:", type=("build", "run"), when="@0.8.29:")
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-joblib@1.0:", type=("build", "run"), when="@0.8.29:")
    depends_on("py-six", type=("build", "run"))
