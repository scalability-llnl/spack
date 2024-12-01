# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dtf(AutotoolsPackage):
    """DTF (Data Transfer Framework) is a general I/O arbitration
    middleware designed for multi-component applications that use
    file-base component coupling.

    DTF works for applications that use the Parallel netCDF (PnetCDF)
    library for file I/O. It allows the user to transparently replace
    file I/O with sending the data directly between the components.
    """

    homepage = "https://github.com/maneka07/DTF"
    git = "https://github.com/maneka07/DTF.git"

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("cxx", default=True, description="Build pnetcdf the C++ Interface")
    variant("fortran", default=True, description="Build pnetcdf the Fortran Interface")

    depends_on("mpi")
    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("perl", type="build")

    configure_directory = "pnetcdf"

    def setup_build_environment(self, env):
        dtf_srcdir = join_path(self.stage.source_path, "libdtf")
        env.append_path("LD_LIBRARY_PATH", self.prefix.lib)
        env.append_path("LD_LIBRARY_PATH", dtf_srcdir)

    @run_before("autoreconf")
    def build_dtf(self):
        with working_dir("libdtf"):
            make("all", "MPICC={0}".format(self.spec["mpi"].mpicc))

    def configure_args(self):
        dtf_srcdir = join_path(self.stage.source_path, "libdtf")
        args = ["CFLAGS=-I{0}".format(dtf_srcdir), "LDFLAGS=-L{0} -ldtf".format(dtf_srcdir)]
        args += self.enable_or_disable("cxx")
        args += self.enable_or_disable("fortran")
        return args

    def install(self, spec, prefix):
        with working_dir("pnetcdf"):
            make("install")
        with working_dir("libdtf"):
            install("libdtf.*", prefix.lib)
            install("dtf.h", prefix.include)
        install_tree("doc", prefix.doc)
        install_tree("example", prefix.example)
        install("COPYRIGHT", prefix)
