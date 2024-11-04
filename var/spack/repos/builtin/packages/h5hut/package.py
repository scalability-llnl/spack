# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class H5hut(AutotoolsPackage):
    """H5hut (HDF5 Utility Toolkit).
    High-Performance I/O Library for Particle-based Simulations."""

    homepage = "https://amas.psi.ch/H5hut/"
    url = "https://amas.web.psi.ch/Downloads/H5hut/H5hut-2.0.0rc3.tar.gz"
    git = "https://gitlab.psi.ch/H5hut/src.git"

    version("2.0.0rc3", sha256="1ca9a9478a99e1811ecbca3c02cc49258050d339ffb1a170006eab4ab2a01790")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=True, description="Enable Fortran support")
    variant("mpi", default=True, description="Enable MPI support")

    depends_on("autoconf", type="build", when="build_system=autotools")
    depends_on("automake", type="build", when="build_system=autotools")
    depends_on("libtool", type="build", when="build_system=autotools")

    depends_on("mpi", when="+mpi")
    # h5hut +mpi uses the obsolete function H5Pset_fapl_mpiposix:
    depends_on("hdf5@1.8:+mpi", when="+mpi")
    depends_on("hdf5@1.8:", when="~mpi")

    # If built in parallel, the following error message occurs:
    # install: .libs/libH5hut.a: No such file or directory
    parallel = False

    @run_before("configure")
    def validate(self):
        """Checks if Fortran compiler is available."""

        if self.spec.satisfies("+fortran") and not self.compiler.fc:
            raise RuntimeError("Cannot build Fortran variant without a Fortran compiler.")

    def flag_handler(self, name, flags):
        build_system_flags = []
        if name == "cflags" and self.spec["hdf5"].satisfies("@1.12:"):
            build_system_flags = ["-DH5_USE_110_API"]
        return flags, None, build_system_flags

    def autoreconf(self, spec, prefix):
        which("bash")("autogen.sh")

    def configure_args(self):
        spec = self.spec
        config_args = ["--enable-shared"]

        if spec.satisfies("+fortran"):
            config_args.append("--enable-fortran")

        if spec.satisfies("+mpi"):
            config_args.extend(
                [
                    "--enable-parallel",
                    "CC={0}".format(spec["mpi"].mpicc),
                    "CXX={0}".format(spec["mpi"].mpicxx),
                ]
            )

            if spec.satisfies("+fortran"):
                config_args.append("FC={0}".format(spec["mpi"].mpifc))

        return config_args
