# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyAdios(PythonPackage):
    """NumPy bindings of ADIOS1"""

    homepage = "https://csmd.ornl.gov/adios"
    url = "https://github.com/ornladios/ADIOS/archive/v1.13.1.tar.gz"
    git = "https://github.com/ornladios/ADIOS.git"

    maintainers("ax3l", "jychoi-hpc")

    version("develop", branch="master")
    version("1.13.1", sha256="b1c6949918f5e69f701cabfe5987c0b286793f1057d4690f04747852544e157b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")

    for v in ["1.13.1", "develop"]:
        depends_on(
            "adios@{0} ~mpi".format(v), when="@{0} ~mpi".format(v), type=["build", "link", "run"]
        )
        depends_on(
            "adios@{0} +mpi".format(v), when="@{0} +mpi".format(v), type=["build", "link", "run"]
        )

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=["build", "run"])
    depends_on("mpi", when="+mpi")
    depends_on("py-mpi4py", type=["run"], when="+mpi")
    depends_on("py-cython", type=["build"])

    build_directory = "wrappers/numpy"

    def patch(self):
        if "+mpi" in self.spec:
            with working_dir(self.build_directory):
                copy("setup_mpi.py", "setup.py")

    @run_before("install")
    def build_clib(self):
        # calls: make CYTHON=y [MPI=y] python
        args = ["CYTHON=y"]
        if "+mpi" in self.spec:
            args += ["MPI=y"]
        args += ["python"]
        with working_dir(self.build_directory):
            os.remove("adios.cpp")
            os.remove("adios_mpi.cpp")
            make(*args, parallel=False)
