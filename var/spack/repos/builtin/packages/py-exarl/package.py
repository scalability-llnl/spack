# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyExarl(PythonPackage):
    """A scalable software framework for reinforcement learning environments
    and agents/policies used for the Design and Control applications"""

    homepage = "https://github.com/exalearn/EXARL"
    git = "https://github.com/exalearn/EXARL.git"

    maintainers("cmahrens")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("develop", branch="develop")
    version("update-spack", branch="update-spack")
    version("0.1.0", tag="v0.1.0", commit="5f5b99884a92f86ea9f637524eca6f4393b9635f")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("git-lfs", type=("build"))
    depends_on("py-setuptools", type=("build"))

    depends_on("py-ase", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("py-lmfit", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-keras", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-tensorflow", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))

    phases = ["install"]
