# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyLvis(PythonPackage):
    """Python API for LVIS dataset."""

    pypi = "lvis/lvis-0.5.3.tar.gz"

    version("0.5.3", sha256="55aeeb84174abea2ed0d6985a8e93aa9bdbb60c61c6db130c8269a275ef61a6e")

    depends_on("py-setuptools", type="build")
    depends_on("py-cycler@0.10:", type=("build", "run"))
    depends_on("py-cython@0.29.12:", type=("build", "run"))
    depends_on("py-kiwisolver@1.1:", type=("build", "run"))
    depends_on("py-matplotlib@3.1.1:", type=("build", "run"))
    depends_on("py-numpy@1.18.2:", type=("build", "run"))
    depends_on("opencv@4.1.0.25:+python3", type=("build", "run"))
    depends_on("py-pyparsing@2.4.0:", type=("build", "run"))
    depends_on("py-python-dateutil@2.8:", type=("build", "run"))
    depends_on("py-six@1.12:", type=("build", "run"))

    # imported at lvis/lvis.py:15
    depends_on("py-pycocotools", type=("build", "run"))

    def patch(self):
        os.rename(
            join_path(self.stage.source_path, "lvis.egg-info", "requires.txt"),
            join_path(self.stage.source_path, "requirements.txt"),
        )
