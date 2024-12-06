# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmoteVariants(PythonPackage):
    """Variants of the synthetic minority oversampling technique (SMOTE) for
    imbalanced learning"""

    homepage = "https://github.com/analyticalmindsltd/smote_variants"
    pypi = "smote_variants/smote_variants-0.7.3.tar.gz"

    version("0.7.3", sha256="69497c764f101a76e8a3d4a9c80176704375c7aa5e26914f19222b59fb03b890")

    depends_on("python@3.5:", type=("build", "run"))

    depends_on("py-wheel@0.33.4:", type="build")
    depends_on("py-setuptools@41.0.1:", type="build")
    depends_on("py-pytest-runner", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-minisom", type=("build", "run"))
    depends_on("py-tensorflow", type=("build", "run"))
    depends_on("py-keras", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("mkl")
    depends_on("py-metric-learn", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    # Not including statistics, because is only needed for python 2
