# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack.package import *


class Abacus(MakefilePackage):
    """ABACUS (Atomic-orbital Based Ab-initio Computation at UStc)
    is an open-source computer code package aiming
    for large-scale electronic-structure simulations
    from first principles"""

    maintainers("bitllion")

    homepage = "http://abacus.ustc.edu.cn/"
    git = "https://github.com/abacusmodeling/abacus-develop.git"
    url = "https://github.com/abacusmodeling/abacus-develop/archive/refs/tags/v2.2.1.tar.gz"

    license("LGPL-3.0-or-later")

    version("develop", branch="develop")
    version("2.2.3", sha256="88dbf6a3bdd907df3e097637ec8e51fde13e2f5e0b44f3667443195481320edf")
    version("2.2.2", sha256="4a7cf2ec6e43dd5c53d5f877a941367074f4714d93c1977a719782957916169e")
    version("2.2.1", sha256="14feca1d8d1ce025d3f263b85ebfbebc1a1efff704b6490e95b07603c55c1d63")
    version("2.2.0", sha256="09d4a2508d903121d29813a85791eeb3a905acbe1c5664b8a88903f8eda64b8f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Enable OpenMP support")

    depends_on("elpa+openmp", when="+openmp")
    depends_on("elpa~openmp", when="~openmp")
    depends_on("cereal")
    depends_on("libxc")
    depends_on("fftw")
    # MPI is a necessary dependency
    depends_on("mpi", type=("build", "link", "run"))
    depends_on("mkl")

    build_directory = "source"

    def edit(self, spec, prefix):
        if spec.satisfies("+openmp"):
            inc_var = "_openmp-"
            system_var = "ELPA_LIB = -L${ELPA_LIB_DIR} -lelpa_openmp -Wl, -rpath=${ELPA_LIB_DIR}"
        else:
            inc_var = "-"
            system_var = "ELPA_LIB = -L${ELPA_LIB_DIR} -lelpa -Wl,-rpath=${ELPA_LIB_DIR}"

        tempInc = (
            "\
FORTRAN = ifort\n\
CPLUSPLUS = icpc\n\
CPLUSPLUS_MPI = mpiicpc\n\
LAPACK_DIR = $(MKLROOT)\n\
FFTW_DIR = %s\n\
ELPA_DIR = %s\n\
ELPA_INCLUDE = -I${ELPA_DIR}/include/elpa%s%s\n\
CEREAL_DIR = %s\n\
OBJ_DIR = obj\n\
OBJ_DIR_serial = obj\n\
NP      = 14\n"
            % (
                spec["fftw"].prefix,
                spec["elpa"].prefix,
                inc_var,
                f"{spec['elpa'].version}",
                spec["cereal"].prefix,
            )
        )

        with open(self.build_directory + "/Makefile.vars", "w") as f:
            f.write(tempInc)

        lineList = []
        Pattern1 = re.compile("^ELPA_INCLUDE_DIR")
        Pattern2 = re.compile("^ELPA_LIB\\s*= ")
        with open(self.build_directory + "/Makefile.system", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                elif Pattern1.search(line):
                    pass
                elif Pattern2.search(line):
                    pass
                else:
                    lineList.append(line)
        with open(self.build_directory + "/Makefile.system", "w") as f:
            for i in lineList:
                f.write(i)

        with open(self.build_directory + "/Makefile.system", "a") as f:
            f.write(system_var)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
