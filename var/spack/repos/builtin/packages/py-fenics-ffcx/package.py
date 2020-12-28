# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsFfcx(PythonPackage):
    """Next generation FEniCS Form Compiler"""

    homepage = "https://github.com/FEniCS/ffcx"
    git = "https://github.com/FEniCS/ffcx.git"
    maintainers = ["js947", "chrisrichardson"]

    version("master", branch="master")

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-fenics-ufl@master", type=("build", "run"))
    depends_on("py-fenics-fiat@master", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
