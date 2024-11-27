# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mpich(AutotoolsPackage):
    """MPICH is a high performance and widely portable implementation of
    the Message Passing Interface (MPI) standard."""

    homepage = "http://www.mpich.org"
    url = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
    git = "https://github.com/pmodels/mpich.git"
    list_url = "http://www.mpich.org/static/downloads/"
    list_depth = 1

    version("develop", submodules=True)
    version("3.2.1", md5="e175452f4d61646a52c73031683fc375")
    version("3.2", md5="f414cfa77099cd1fa1a5ae4e22db508a")
    version("3.1.4", md5="2ab544607986486562e076b83937bba2")
    version("3.1.3", md5="93cb17f91ac758cbf9174ecb03563778")
    version("3.1.2", md5="7fbf4b81dcb74b07ae85939d1ceee7f1")
    version("3.1.1", md5="40dc408b1e03cc36d80209baaa2d32b7")
    version("3.1", md5="5643dd176499bfb7d25079aaff25f2ec")
    version("3.0.4", md5="9c5d5d4fe1e17dd12153f40bc5b6dbc0")

    variant("hydra", default=True, description="Build the hydra process manager")
    variant("pmi", default=True, description="Build with PMI support")
    variant("romio", default=True, description="Enable ROMIO MPI I/O implementation")
    variant("verbs", default=False, description="Build support for OpenFabrics verbs.")
    variant(
        "device",
        default="ch3",
        description="""Abstract Device Interface (ADI)
implementation. The ch4 device is currently in experimental state""",
        values=("ch3", "ch4"),
        multi=False,
    )
    variant(
        "netmod",
        default="tcp",
        description="""Network module. Only single netmod builds are
supported. For ch3 device configurations, this presumes the
ch3:nemesis communication channel. ch3:sock is not supported by this
spack package at this time.""",
        values=("tcp", "mxm", "ofi", "ucx"),
        multi=False,
    )

    provides("mpi")
    provides("mpi@:3.0", when="@3:")
    provides("mpi@:1.3", when="@1:")

    filter_compiler_wrappers("mpicc", "mpicxx", "mpif77", "mpif90", "mpifort", relative_root="bin")

    # fix MPI_Barrier segmentation fault
    # see https://lists.mpich.org/pipermail/discuss/2016-May/004764.html
    # and https://lists.mpich.org/pipermail/discuss/2016-June/004768.html
    patch("mpich32_clang.patch", when="@=3.2%clang")

    depends_on("findutils", type="build")

    depends_on("libfabric", when="netmod=ofi")

    conflicts("device=ch4", when="@:3.2")
    conflicts("netmod=ofi", when="@:3.1.4")
    conflicts("netmod=ucx", when="device=ch3")
    conflicts("netmod=mxm", when="device=ch4")
    conflicts("netmod=mxm", when="@:3.1.3")
    conflicts("netmod=tcp", when="device=ch4")

    def setup_dependent_build_environment(self, env, dependent_spec):
        # TUTORIAL: set the following variables for dependents:
        #
        # MPICC=join_path(self.prefix.bin, 'mpicc')
        # MPICXX=join_path(self.prefix.bin, 'mpic++')
        # MPIF77=join_path(self.prefix.bin, 'mpif77')
        # MPIF90=join_path(self.prefix.bin, 'mpif90')
        # MPICH_CC=spack_cc
        # MPICH_CXX=spack_cxx
        # MPICH_F77=spack_f77
        # MPICH_F90=spack_fc
        # MPICH_FC=spack_fc
        pass

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = join_path(self.prefix.bin, "mpicc")
        self.spec.mpicxx = join_path(self.prefix.bin, "mpic++")
        self.spec.mpifc = join_path(self.prefix.bin, "mpif90")
        self.spec.mpif77 = join_path(self.prefix.bin, "mpif77")

        self.spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, "libmpicxx.{0}".format(dso_suffix)),
            join_path(self.prefix.lib, "libmpi.{0}".format(dso_suffix)),
        ]

    def autoreconf(self, spec, prefix):
        """Not needed usually, configure should be already there"""
        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path):
            return
        # Else bootstrap with autotools
        bash = which("bash")
        bash("./autogen.sh")

    @run_before("autoreconf")
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError("Mpich requires both C and Fortran compilers!")

    def configure_args(self):
        spec = self.spec
        config_args = [
            "--enable-shared",
            "--with-pm={0}".format("hydra" if "+hydra" in spec else "no"),
            "--with-pmi={0}".format("yes" if "+pmi" in spec else "no"),
            "--{0}-romio".format("enable" if "+romio" in spec else "disable"),
            "--{0}-ibverbs".format("with" if "+verbs" in spec else "without"),
        ]

        # setup device configuration
        device_config = ""
        if "device=ch4" in spec:
            device_config = "--with-device=ch4:"
        elif "device=ch3" in spec:
            device_config = "--with-device=ch3:nemesis:"

        if "netmod=ucx" in spec:
            device_config += "ucx"
        elif "netmod=ofi" in spec:
            device_config += "ofi"
        elif "netmod=mxm" in spec:
            device_config += "mxm"
        elif "netmod=tcp" in spec:
            device_config += "tcp"

        config_args.append(device_config)

        return config_args
