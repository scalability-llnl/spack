# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Modylas(AutotoolsPackage):
    """
    The 'MOlecular DYnamics Software for LArge Systems' (MODYLAS) is
    a general-purpose, molecular dynamics simulation program suited
    to the simulation of very large physical, chemical,
    and biological systems.
    """

    homepage = "https://www.modylas.org"
    url = "file://{0}/MODYLAS_1.0.4.tar.gz".format(os.getcwd())
    manual_download = True

    version("1.0.4", sha256="e0b5cccf8e363c1182eced37aa31b06b1c5b1526da7d449a6142424ac4ea6311")

    variant("mpi", default=True, description="Enable MPI support")

    # to define MPIPARA when +mpi
    patch("makefile.patch")
    # fix no width I in format
    patch("gcc_format.patch", when="%gcc")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("mpi", when="+mpi")

    build_directory = "source"
    configure_directory = "source"

    def setup_build_environment(self, env):
        if self.spec.satisfies("+mpi"):
            env.set("FC", self.spec["mpi"].mpifc, force=True)
        fflags = ["-O3", self.compiler.openmp_flag]
        if self.spec.satisfies("%gcc"):
            fflags.append("-cpp")
        elif self.spec.satisfies("%fj"):
            fflags.append("-Cpp")
        env.set("FCFLAGS", " ".join(fflags))

    def configure_args(self):
        return self.enable_or_disable("mpi")
