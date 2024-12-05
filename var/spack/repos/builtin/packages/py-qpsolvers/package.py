# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQpsolvers(PythonPackage):
    """Unified interface to convex Quadratic Programming (QP) solvers available in
    Python."""

    homepage = "https://github.com/qpsolvers/qpsolvers"
    pypi = "qpsolvers/qpsolvers-3.1.0.tar.gz"

    maintainers("meyersbs")

    license("LGPL-3.0-only")

    version("3.2.0", sha256="770a2b40ff827e251a30df97e9d518fd4859621fc02a323c3b6407cf2fbf4f34")
    version("3.1.0", sha256="f6becafc4667236a67276fa0baee1697c904c37498c5161fa40c605209269b4d")

    depends_on("py-flit-core@2:3", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-ecos@2.0.8:", type=("build", "run"))
    depends_on("py-numpy@1.15.4:", type=("build", "run"))
    depends_on("py-osqp@0.6.2:", type=("build", "run"))
    depends_on("py-scipy@1.2.0:", type=("build", "run"))
    depends_on("py-scs@3.2.0:", type=("build", "run"))
