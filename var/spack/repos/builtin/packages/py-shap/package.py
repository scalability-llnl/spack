# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyShap(PythonPackage):
    """SHAP (SHapley Additive exPlanations): a unified approach
    to explain the output of any machine learning model."""

    homepage = "https://github.com/slundberg/shap/"
    pypi = "shap/shap-0.41.0.tar.gz"

    license("MIT")

    version("0.41.0", sha256="a49ea4d65aadbc845a695fa3d7ea0bdfc8c928b8e213b0feedf5868ade4b3ca5")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-tqdm@4.25.1:", type=("build", "run"))
    depends_on("py-packaging@20.10:", type=("build", "run"))
    depends_on("py-slicer@0.0.7", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("py-cloudpickle", type=("build", "run"))
