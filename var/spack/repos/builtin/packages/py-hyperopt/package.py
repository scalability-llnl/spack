# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHyperopt(PythonPackage):
    """Hyperopt is a Python library for serial and parallel optimization over
    awkward search spaces, which may include real-valued, discrete, and
    conditional dimensions."""

    homepage = "https://hyperopt.github.io/hyperopt/"
    pypi = "hyperopt/hyperopt-0.2.5.tar.gz"

    version("0.2.5", sha256="bc6047d50f956ae64eebcb34b1fd40f186a93e214957f20e87af2f10195295cc")

    variant("spark", default=False, description="SparkTrials")
    variant("mongo", default=False, description="MongoTrials")
    variant("atpe", default=False, description="ATPE")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-networkx@2.2:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-cloudpickle", type=("build", "run"))
    depends_on("py-pyspark", when="+spark", type=("build", "run"))
    depends_on("py-pymongo", when="+mongo", type=("build", "run"))
    depends_on("py-scikit-learn", when="+atpe", type=("build", "run"))
    depends_on("py-lightgbm", when="+atpe", type=("build", "run"))
