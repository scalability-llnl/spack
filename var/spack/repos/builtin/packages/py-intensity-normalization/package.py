# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIntensityNormalization(PythonPackage):
    """Normalize intensities of images from various MRI modalities"""

    homepage = "https://github.com/jcreinhold/intensity-normalization"
    pypi = "intensity-normalization/intensity-normalization-2.1.1.tar.gz"

    license("Apache-2.0")

    version("2.1.1", sha256="686b86754a9a520a03f793cb15c87e945f68ede78ac0ad1b3564c5d5b7ac9486")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build",))
    depends_on("py-pytest-runner", type=("build",))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scikit-fuzzy", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-statsmodels", type=("build", "run"))
