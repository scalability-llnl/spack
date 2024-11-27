# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNistats(PythonPackage):
    """Modeling and Statistical analysis of fMRI data in Python."""

    homepage = "https://github.com/nilearn/nistats"
    pypi = "nistats/nistats-0.0.1rc0.tar.gz"

    version("0.0.1rc0", sha256="dcc4c4e410f542fd72e02e12b3b6531851bae2680d08ad29658b272587ef2f98")
    version("0.0.1b2", sha256="a853149087bafbf1bed12664ed8889a63ff15dde1fb7a9d51e8a094afc8d695d")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.11:", type=("build", "run"))
    depends_on("py-scipy@0.17:", type=("build", "run"))
    depends_on("py-scikit-learn@0.18:", type=("build", "run"))
    depends_on("py-nibabel@2.0.2:", type=("build", "run"))
    # needs +plotting to avoid ModuleNotFoundError:
    # 'nilearn.plotting.js_plotting_utils' when importing nistats.reporting
    # Functionality has been incorporated into py-nilearn@0.7:
    depends_on("py-nilearn+plotting@0.4:0.6", type=("build", "run"))
    depends_on("py-pandas@0.18:", type=("build", "run"))
