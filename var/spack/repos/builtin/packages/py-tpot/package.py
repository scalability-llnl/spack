# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTpot(PythonPackage):
    """
    A Python Automated Machine Learning tool that optimizes machine learning
    pipelines using genetic programming.
    """

    homepage = "https://epistasislab.github.io/tpot/"
    pypi = "tpot/TPOT-0.11.5.tar.gz"

    license("LGPL-3.0-only")

    version("0.11.7", sha256="64ff1845efdec3d9c70b35587f719cc0821722f27d16f542f83bf81f448e3ff1")
    version("0.11.5", sha256="909be08b29165ce48de5e5d2e3fd73fee9aeeaf1030f2e0912ce0f0bd9c3d2f3")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-deap@1.2:", type=("build", "run"))
    depends_on("py-numpy@1.16.3:", type=("build", "run"))
    depends_on("py-scikit-learn@0.22.0:", type=("build", "run"))
    depends_on("py-scipy@1.3.1:", type=("build", "run"))
    depends_on("py-tqdm@4.36.1:", type=("build", "run"))
    depends_on("py-stopit@1.1.1:", type=("build", "run"))
    depends_on("py-pandas@0.24.2:", type=("build", "run"))
    depends_on("py-joblib@0.13.2:", type=("build", "run"))
    depends_on("py-update-checker@0.16:", type=("build", "run"))
    depends_on("py-xgboost@1.1.0:", type=("build", "run"), when="@0.11.7:")
