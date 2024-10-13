# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMgmetis(PythonPackage):
    """METIS partitioner for mesh and graphMETIS partitioner for mesh and graph"""

    homepage = "https://github.com/chiao45/mgmetis"
    git = "https://github.com/chiao45/mgmetis.git"
    maintainers("tech-91")

    license("MIT")

    version("master", branch="master")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.20.0:1.26.4", type=("build", "run"))
    depends_on("py-cython", type=("build"))
    depends_on("py-mpi4py@3.0.3:", type=("build", "run"))
    depends_on("py-pytest")
    depends_on("metis+shared", type="all")
