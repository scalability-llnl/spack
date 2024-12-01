# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCma(PythonPackage):
    """
    Python implementation of CMA-ES Covariance Matrix Adaptation Evolution Str
    ategy for non-linear numerical optimization in Python
    """

    homepage = "https://github.com/CMA-ES/pycma"
    pypi = "cma/cma-3.3.0.tar.gz"

    maintainers("LydDeb")

    version("3.3.0", sha256="b748b8e03f4e7ae816157d7b9bb2fc6b1fb2fee1d5fd3399329b646bb75861ec")

    variant("plotting", default=False, description="Build with matplotlib support.")
    variant(
        "constrained_solution_tracking",
        default=False,
        description="Build with moarchiving support.",
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"), when="+plotting")
    depends_on("py-moarchiving", type=("build", "run"), when="+constrained_solution_tracking")
