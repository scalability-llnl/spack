# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPapermill(PythonPackage):
    """Parametrize and run Jupyter and nteract Notebooks."""

    homepage = "https://github.com/nteract/papermill"
    pypi = "papermill/papermill-2.4.0.tar.gz"

    license("BSD-3-Clause")

    version("2.4.0", sha256="6f8f8a9b06b39677f207c09100c8d386bcf592f0cbbdda9f0f50e81445697627")

    depends_on("py-setuptools", type="build")
    depends_on("py-ansiwrap", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-nbformat@5.1.2:", type=("build", "run"))
    depends_on("py-nbclient@0.2:", type=("build", "run"))
    depends_on("py-tqdm@4.32.2:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-entrypoints", type=("build", "run"))
    depends_on("py-tenacity", type=("build", "run"))
