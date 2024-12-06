# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPybobyqa(PythonPackage):
    """Py-BOBYQA is a flexible package for solving bound-constrained general
    objective minimization, without requiring derivatives of the objective."""

    homepage = "https://github.com/numericalalgorithmsgroup/pybobyqa/"
    pypi = "Py-BOBYQA/Py-BOBYQA-1.3.tar.gz"

    version("1.3", sha256="7b0b27b7b9a7cfef94557c8832c0c30757e86764e32878677427381f0691a8fb")

    depends_on("py-setuptools", type="build")
    depends_on("py-scipy@0.17:", type=("build", "run"))
    depends_on("py-pandas@0.17:", type=("build", "run"))
    depends_on("py-numpy@1.11:", type=("build", "run"))
