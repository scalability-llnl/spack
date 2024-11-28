# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hpddm(Package):
    """High-performance unified framework for domain decomposition methods."""

    homepage = "https://github.com/hpddm/hpddm"
    url = "https://github.com/hpddm/hpddm"
    git = "https://github.com/hpddm/hpddm.git"

    maintainers("corentin-dev")

    license("LGPL-3.0-or-later")

    version("main", branch="main")

    version("2.2.3", commit="54228a5288a38cf1a144df13c96b00ac9240179c")
    version("2.2.2", commit="ff61cf3ced922c2f896ebe1fff1a42f1f2805a3a")
    version("2.2.1", commit="382ee53a2fb9dcb3ff32424a2cbe6dc3cea89514")
    version("2.2.0", commit="5641877b44006c012c7fda0593d44e11c19c1c5b")
    version("2.1.3", commit="32025e4ee75a16fa67399d26dd86910c03910dba")
    version("2.1.2", commit="e58205623814f59bf2aec2e2bab8eafcfbd22466")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("mumps")
    depends_on("hypre")
    depends_on("scalapack")
    depends_on("arpack-ng")
    depends_on("python")

    def configure(self):
        makefile_inc = []
        # cflags = [
        makefile_inc.append("SOLVER ?= MUMPS")
        makefile_inc.append("SUBSOLVER ?= MUMPS")
        makefile_inc.append("EIGENSOLVER ?= ARPACK")
        makefile_inc.append("MPICXX ?= mpic++")
        makefile_inc.append("MPICC ?= mpicc")
        makefile_inc.append("MPIF90 ?= mpif90")
        makefile_inc.append("MPIRUN ?= mpirun -np")

        makefile_inc.append("override CXXFLAGS += -std=c++11 -O3 -fPIC")
        makefile_inc.append("override CFLAGS += -std=c99 -O3")
        makefile_inc.append("INCS =")
        makefile_inc.append("LIBS =")

        makefile_inc.append("HPDDMFLAGS ?= -DHPDM_NUMBERING='C'")

        makefile_inc.append("MUMPS_INCS = ")
        makefile_inc.append("PYTHON_INCS = ")
        makefile_inc.append("BLAS_LIBS = -lopenblas")
        makefile_inc.append("ARPACK_LIBS = -larpack")
        makefile_inc.append("SCALAPACK_LIBS = -lscalapack")
        makefile_inc.append(
            " ".join(
                [
                    "MUMPS_LIBS",
                    "=",
                    "-lcmumps",
                    "-ldmumps",
                    "-lsmumps",
                    "-lzmumps",
                    "-lmumps_common",
                    "-lpord",
                    "-fopenmp",
                ]
            )
        )
        makefile_inc.append("HYPRE_LIBS = -lHYPRE")
        makefile_inc.append("PYTHON_LIBS = -lpython3")

        with working_dir("."):
            with open("Makefile.inc", "w") as fh:
                fh.write("\n".join(makefile_inc))

    def patch(self):
        self.configure()

    def install(self, spec, prefix):
        make()
        install_tree("include", prefix.include)
        # make('install')
