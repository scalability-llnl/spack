# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsBasix(PythonPackage):
    """Python basis evaluation library for Next generation FEniCS problem solving
    environment"""

    homepage = "https://github.com/FEniCS/basix"
    git = "https://github.com/FEniCS/basix.git"
    maintainers = ["chrisrichardson", "mscroggs"]

    version("main", branch="main")

    depends_on("fenics-basix@main", type=("build", "run"))
    depends_on("python@3.6:", type=('build', 'run'))
    depends_on("eigen@3.3.7:")
    depends_on("py-setuptools", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("py-pybind11@2.6.2:", type="build")

    phases = ['build_ext', 'build', 'install']

    build_directory = 'python'
