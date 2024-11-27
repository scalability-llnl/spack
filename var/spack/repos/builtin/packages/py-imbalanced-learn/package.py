# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImbalancedLearn(PythonPackage):
    """imbalanced-learn is a python package offering a number of re-sampling
    techniques commonly used in datasets showing strong between-class imbalance.
    It is compatible with scikit-learn and is part of scikit-learn-contrib
    projects."""

    homepage = "https://github.com/scikit-learn-contrib/imbalanced-learn"
    pypi = "imbalanced-learn/imbalanced-learn-0.10.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("0.10.1", sha256="bc7609619ec3c38c442292928239ad3d10b5deb0af8a29c83822b7b57b319f8b")

    # From setup.py:
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.17.3:", type=("build", "run"))
    depends_on("py-scipy@1.3.2:", type=("build", "run"))
    depends_on("py-scikit-learn@1.0.2:", type=("build", "run"))

    variant("optional", default=False, description="Enable optional dependencies.")
    depends_on("py-pandas@1.0.5:", when="+optional", type=("build", "run"))
    depends_on("py-tensorflow@2.4.3:", when="+optional", type=("build", "run"))
    depends_on("py-keras@2.4.3:", when="+optional", type=("build", "run"))

    # From https://imbalanced-learn.org/stable/install.html#getting-started:
    depends_on("py-joblib@1.1.1:", type=("build", "run"))
    depends_on("py-threadpoolctl@2.0.0:", type=("build", "run"))
    depends_on("py-cython@0.29.24:", type="build")
