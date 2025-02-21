# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUncertaintyToolbox(PythonPackage):
    """Uncertainty Toolbox: a python toolbox for predictive uncertainty quantification,
    calibration, metrics, and visualization."""

    homepage = "https://uncertainty-toolbox.github.io/"
    pypi = "uncertainty-toolbox/uncertainty-toolbox-0.1.1.tar.gz"

    license("MIT")

    version("0.1.1", sha256="d9389112bd431edc8b6e44c5b12405dea8f86063ff9b79f0bb178e5ac76bcfa5")

    with default_args(type="build"):
        depends_on("py-flit-core@3.2:3")
        depends_on("py-setuptools")

    with default_args(type=("build", "run")):
        depends_on("py-numpy@1.19:")
        depends_on("py-scipy@1.5:")
        depends_on("py-matplotlib@3.2.2:")
        depends_on("py-scikit-learn@0.23.1:")
        depends_on("py-tqdm@4.54:")
