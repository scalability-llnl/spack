# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.hooks.sbang import filter_shebang
from spack.package import *


class Grackle(Package):
    """Grackle is a chemistry and radiative cooling library for astrophysical
    simulations with interfaces for C, C++, and Fortran codes. It is a
    generalized and trimmed down version of the chemistry network of the Enzo
    simulation code
    """

    homepage = "http://grackle.readthedocs.io/en/latest/"
    url = "https://github.com/grackle-project/grackle/archive/refs/tags/grackle-3.1.tar.gz"

    version("3.1", sha256="5705985a70d65bc2478cc589ca26f631a8de90e3c8f129a6b2af69db17c01079")
    version("3.0", sha256="41e9ba1fe18043a98db194a6f5b9c76a7f0296a95a457d2b7d73311195b7d781")
    version("2.2", sha256="5855cb0f93736fd8dd47efeb0abdf36af9339ede86de7f895f527513566c0fae")
    version("2.0.1", sha256="bcdf6b3ff7b7515ae5e9f1f3369b2690ed8b3c450040e92a03e40582f57a0864")

    variant("float", default=False, description="Build with float")

    depends_on("libtool", when="@2.2:")

    depends_on("c", type="build")
    depends_on("fortran", type="build")
    depends_on("tcsh", type="build")
    depends_on("mpi")
    depends_on("hdf5+mpi")

    parallel = False

    @run_before("install")
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
        can fix up the path to the tcsh binary.
        """
        tcsh = self.spec["tcsh"].command
        with working_dir(self.stage.source_path):
            match = "^#!/bin/csh.*"
            substitute = f"#!{tcsh}"
            filter_file(match, substitute, "configure")
            # Since scripts are run during installation, we need to add sbang
            filter_shebang("configure")

    def install(self, spec, prefix):
        template_name = "{0.architecture}-{0.compiler.name}"
        grackle_architecture = template_name.format(spec)
        link_variables = (
            "MACH_AR = ar" if spec.version < Version("2.2") else "MACH_LIBTOOL = libtool"
        )
        substitutions = {
            "@ARCHITECTURE": grackle_architecture,
            "@CC": spec["mpi"].mpicc,
            "@CXX": spec["mpi"].mpicxx,
            "@FC": spec["mpi"].mpifc,
            "@F77": spec["mpi"].mpif77,
            "@STDCXX_LIB": " ".join(self.compiler.stdcxx_libs),
            "@HDF5_ROOT": spec["hdf5"].prefix,
            "@PREFIX": prefix,
            "@LINK_VARIABLES_DEFINITION": link_variables,
        }

        template = join_path(os.path.dirname(__file__), "Make.mach.template")
        makefile = join_path(
            self.stage.source_path, "src", "clib", "Make.mach.{0}".format(grackle_architecture)
        )
        copy(template, makefile)
        for key, value in substitutions.items():
            filter_file(key, value, makefile)

        configure()
        with working_dir(join_path(self.stage.source_path, "src", "clib")):
            make("clean")
            make("machine-{0}".format(grackle_architecture))
            make("opt-high")
            if spec.satisfies("+float"):
                make("precision-32")
            make("show-config")
            make()
            mkdirp(prefix.lib)
            make("install")
