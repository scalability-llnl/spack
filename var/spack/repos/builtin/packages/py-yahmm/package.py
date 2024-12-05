# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYahmm(PythonPackage):
    """YAHMM is a HMM package for Python, implemented in Cython for speed."""

    pypi = "yahmm/yahmm-1.1.3.zip"

    license("MIT")

    version("1.1.3", sha256="fe3614ef96da9410468976756fb93dc8235485242c05df01d8e5ed356a7dfb43")
    version("1.1.2", sha256="5e81077323dc6da9fb792169b639f29e5293b0c8272e4c22b204ca95ac0df90a")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.20.1:", type=("build", "run"))
    depends_on("py-numpy@1.8.0:", type=("build", "run"))
    depends_on("py-scipy@0.13.3:", type=("build", "run"))
    depends_on("py-matplotlib@1.3.1:", type=("build", "run"))
    depends_on("py-networkx@1.8.1:", type=("build", "run"))
