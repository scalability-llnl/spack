# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPylops(PythonPackage):
    """Many useful operators, however, do not lend themselves to an explicit
    matrix representation when used to solve large-scale problems. PyLops operators,
    on the other hand, still represent a matrix and can be treated in a similar way,
    but do not rely on the explicit creation of a dense (or sparse) matrix itself.
    Conversely, the forward and adjoint operators are represented by small pieces of
    codes that mimic the effect of the matrix on a vector or another matrix."""

    pypi = "pylops/pylops-1.12.0.tar.gz"
    git = "https://github.com/PyLops/pylops.git"

    maintainers("archxlith")

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("1.12.0", sha256="0e9caef46bbef9691acd133cb9b6d13e19510e8682aaa8f4eb15d9bd9ff9ebb6")
    version("1.11.1", sha256="87010358b1119ebe1f8a601b2768d16d7bd26d55bd0c91a6e83db763e5715f7c")

    variant("advanced", default=False, description="Install optional libraries")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-numpy@1.15:", type=("build", "run"))
    depends_on("py-scipy@1.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-llvmlite", when="+advanced", type=("build", "run"))
    depends_on("py-numba", when="+advanced", type=("build", "run"))
    depends_on("py-pyfftw", when="+advanced", type=("build", "run"))
    depends_on("py-pywavelets", when="+advanced", type=("build", "run"))
    depends_on("py-scikit-fmm", when="+advanced", type=("build", "run"))
    depends_on("py-spgl1", when="+advanced", type=("build", "run"))
