# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBandit(PythonPackage):
    """Security oriented static analyser for python code."""

    homepage = "https://bandit.readthedocs.io/en/latest/"
    pypi = "bandit/bandit-1.7.0.tar.gz"

    version("1.7.0", sha256="8a4c7415254d75df8ff3c3b15cfe9042ecee628a1e40b44c15a98890fbfc2608")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pbr@2.0.0:", type="build")
    depends_on("py-gitpython@1.0.1:", type=("build", "run"))
    depends_on("py-pyyaml@5.3.1:", type=("build", "run"))
    depends_on("py-six@1.10.0:", type=("build", "run"))
    depends_on("py-stevedore@1.20.0:", type=("build", "run"))
    depends_on("py-colorama@0.3.9:", when="platform=win32", type=("build", "run"))
