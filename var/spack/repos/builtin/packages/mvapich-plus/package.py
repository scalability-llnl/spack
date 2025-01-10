# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools
import os.path
import re
import sys
import subprocess
from spack.package import *


class MvapichPlus(AutotoolsPackage):
    """Mvapich is a High-Performance MPI Library for clusters with diverse
    networks (InfiniBand, Omni-Path, Ethernet/iWARP, and RoCE) and computing
    platforms (x86 (Intel and AMD), ARM and OpenPOWER)"""

    homepage = "https://mvapich.cse.ohio-state.edu/userguide/userguide_spack/"
    url = "https://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich-3.0.tar.gz"
    list_url = "https://mvapich.cse.ohio-state.edu/downloads/"

    maintainers("natshineman", "harisubramoni", "MatthewLieber")

    executables = ["^mpiname$", "^mpichversion$"]

    license("Unlicense")

    # Prefer the latest stable release
    version("4.0", sha256="942156804425752ab8b7884a6995581d7d9e93f58025ca71b58e6412eb766eae")

    provides("mpi")
    provides("mpi@:3.1")

    variant("wrapperrpath", default=True, description="Enable wrapper rpath")
    variant("debug", default=False, description="Enable debug info and error messages at run-time")

    variant("cuda", default=True, description="Enable CUDA extension")

    variant("regcache", default=True, description="Enable memory registration cache")

    # Accepted values are:
    #   single      - No threads (MPI_THREAD_SINGLE)
    #   funneled    - Only the main thread calls MPI (MPI_THREAD_FUNNELED)
    #   serialized  - User serializes calls to MPI (MPI_THREAD_SERIALIZED)
    #   multiple    - Fully multi-threaded (MPI_THREAD_MULTIPLE)
    #   runtime     - Alias to "multiple"
    variant(
        "threads",
        default="multiple",
        values=("single", "funneled", "serialized", "multiple"),
        multi=False,
        description="Control the level of thread support",
    )
    variant(
        "nvidia_arch",
        default="Volta",
        values=("Volta", "Ampere","Hopper"),
        multi=False,
        description="Nvidia GPU Arch",
    )
    # 32 is needed when job size exceeds 32768 cores
    variant(
        "ch3_rank_bits",
        default="32",
        values=("16", "32"),
        multi=False,
        description="Number of bits allocated to the rank field (16 or 32)",
    )
    variant(
        "pmi_version",
        description="Which pmi version to be used. If using pmi2 add it to your CFLAGS",
        default="simple",
        values=("simple", "pmi2"),
        multi=False,
    )

    variant(
        "process_managers",
        description="List of the process managers to activate",
        values=disjoint_sets(("auto",), ("slurm",), ("hydra", "gforker", "remshell"))
        .with_error("'slurm' or 'auto' cannot be activated along with " "other process managers")
        .with_default("auto")
        .with_non_feature_values("auto"),
    )

    variant(
        "netmod",
        description="Select the netmod to be enabled for this build."
        "For IB/RoCE systems, use the ucx netmod, for interconnects supported "
        "by libfabrics, use the ofi netmod. For more info, visit the "
        "homepage url.",
        default="ofi",
        values=("ofi", "ucx"),
        multi=False,
    )

    variant(
        "alloca", default=False, description="Use alloca to allocate temporary memory if available"
    )

    variant(
        "file_systems",
        description="List of the ROMIO file systems to activate",
        values=auto_or_any_combination_of("lustre", "gpfs", "nfs", "ufs"),
    )

    depends_on("findutils", type="build")
    depends_on("bison", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("zlib-api")
    depends_on("libpciaccess", when=(sys.platform != "darwin"))
    depends_on("libxml2")
    depends_on("cuda", when="+cuda",type=("build", "link"))
    depends_on("libfabric", when="netmod=ofi")
    depends_on("slurm", when="process_managers=slurm")
    depends_on("ucx", when="netmod=ucx")
    depends_on("hip@3.9.0:", when="+rocm")
    depends_on("rccl", when="+rocm")
    variant("rocm", description="Enable/Disable support for ROCM", default=False)
    conflicts("+cuda +rocm", msg="MVAPICH2-GDR can only be built with either CUDA or ROCm")
    conflicts("~cuda ~rocm", msg="MVAPICH2-GDR must be built with either CUDA or ROCm")
    conflicts(
        "process_managers=slurm pmi_version=simple",
        msg="MVAPICH2-GDR can not be built with slurm and simple pmi",
    )

    with when("process_managers=slurm"):
        conflicts("pmi_version=pmi2")

    with when("process_managers=auto"):
        conflicts("pmi_version=pmi2")

    filter_compiler_wrappers("mpicc", "mpicxx", "mpif77", "mpif90", "mpifort", relative_root="bin")

    @classmethod
    def determine_version(cls, exe):
        if exe.endswith("mpichversion"):
            output = Executable(exe)(output=str, error=str)
            match = re.search(r"^MVAPICH2 Version:\s*(\S+)", output)
        elif exe.endswith("mpiname"):
            output = Executable(exe)("-a", output=str, error=str)
            match = re.search(r"^MVAPICH2 (\S+)", output)
        return match.group(1) if match else None
  @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ["libmpi"]

        if "cxx" in query_parameters:
            libraries = ["libmpicxx"] + libraries

        return find_libraries(libraries, root=self.prefix, shared=True, recursive=True)

    @property
    def process_manager_options(self):
        spec = self.spec

        other_pms = []
        for x in ("hydra", "gforker", "remshell"):
            if "process_managers={0}".format(x) in spec:
                other_pms.append(x)

        opts = []
        if len(other_pms) > 0:
            opts = ["--with-pm=%s" % ":".join(other_pms)]

        # See: http://slurm.schedmd.com/mpi_guide.html#mvapich2
        if "process_managers=slurm" in spec:
            opts = [
                "--with-pm=slurm",
        #        "--with-pmi=simple",
                "--with-slurm={0}".format(spec["slurm"].prefix),
                "CFLAGS=-I{0}/include/slurm".format(spec["slurm"].prefix),
            ]
        if "none" in spec.variants["process_managers"].value:
            opts = ["--with-pm=none"]

        return opts

    @property
    def network_options(self):
        opts = []
        # From here on I can suppose that only one variant has been selected
        if "netmod=ofi" in self.spec:
            opts = ["--with-device=ch4:ofi"]
        elif "netmod=ucx" in self.spec:
            opts = ["--with-device=ch4:ucx"]
        return opts

    @property
    def file_system_options(self):
        spec = self.spec

        fs = []
        for x in ("lustre", "gpfs", "nfs", "ufs"):
            if "file_systems={0}".format(x) in spec:
                fs.append(x)

        opts = []
        if len(fs) > 0:
            opts.append("--with-file-system=%s" % "+".join(fs))

        return opts

    def flag_handler(self, name, flags):
        if name == "fflags":
            # https://bugzilla.redhat.com/show_bug.cgi?id=1795817
            if self.spec.satisfies("%gcc@10:"):
                if flags is None:
                    flags = []
                flags.append("-fallow-argument-mismatch")

        return (flags, None, None)

    def setup_build_environment(self, env):
        # mvapich2 configure fails when F90 and F90FLAGS are set
        env.unset("F90")
        env.unset("F90FLAGS")
        if "+cuda" in self.spec:
            env.prepend_path("PATH",self.spec["cuda"].prefix+"/bin")
            env.prepend_path("LIBRARY_PATH", self.spec["cuda"].prefix+"/lib")
            env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix+"/lib")
            env.prepend_path("LIBRARY_PATH", self.spec["cuda"].prefix+"/lib64")
            env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix+"/lib64")
            env.prepend_path("C_INCLUDE_PATH", self.spec["cuda"].prefix+"/include")
            env.append_path("CPATH", self.spec["cuda"].prefix+"/include")
            env.prepend_path("CPLUS_INCLUDE_PATH", self.spec["cuda"].prefix+"/include")
            env.set("CUDA_HOME", self.spec["cuda"].prefix)
            env.set("CUDA_ROOT", self.spec["cuda"].prefix)
        if "+rocm" in self.spec:
            env.prepend_path("PATH",self.spec["hip"].prefix+"/bin")
            env.prepend_path("LIBRARY_PATH", self.spec["hip"].prefix+"/lib")
            env.prepend_path("LD_LIBRARY_PATH", self.spec["hip"].prefix+"/lib")
            env.prepend_path("LIBRARY_PATH", self.spec["hip"].prefix+"/lib64")
            env.prepend_path("LD_LIBRARY_PATH", self.spec["hip"].prefix+"/lib64")
            env.prepend_path("C_INCLUDE_PATH", self.spec["hip"].prefix+"/include")
            env.append_path("CPATH", self.spec["hip"].prefix+"/include")
            env.prepend_path("CPLUS_INCLUDE_PATH", self.spec["hip"].prefix+"/include")
            env.set("CUDA_HOME", self.spec["hip"].prefix)
            env.set("CUDA_ROOT", self.spec["hip"].prefix)

    def setup_run_environment(self, env):
        env.set("MPI_ROOT", self.prefix)

        # Because MPI functions as a compiler, we need to treat it as one and
        # add its compiler paths to the run environment.
        self.setup_compiler_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_compiler_environment(env)

        # use the Spack compiler wrappers under MPI
        env.set("MPICH_CC", spack_cc)
        env.set("MPICH_CXX", spack_cxx)
        env.set("MPICH_F77", spack_f77)
        env.set("MPICH_F90", spack_fc)
        env.set("MPICH_FC", spack_fc)

    def setup_compiler_environment(self, env):
        # For Cray MPIs, the regular compiler wrappers *are* the MPI wrappers.
        # Cray MPIs always have cray in the module name, e.g. "cray-mvapich"
        if self.spec.satisfies("platform=cray"):
            env.set("MPICC", spack_cc)
            env.set("MPICXX", spack_cxx)
            env.set("MPIF77", spack_fc)
            env.set("MPIF90", spack_fc)
        else:
            env.set("MPICC", join_path(self.prefix.bin, "mpicc"))
            env.set("MPICXX", join_path(self.prefix.bin, "mpicxx"))
            env.set("MPIF77", join_path(self.prefix.bin, "mpif77"))
            env.set("MPIF90", join_path(self.prefix.bin, "mpif90"))

    def setup_dependent_package(self, module, dependent_spec):
        # For Cray MPIs, the regular compiler wrappers *are* the MPI wrappers.
        # Cray MPIs always have cray in the module name, e.g. "cray-mvapich"
        if self.spec.satisfies("platform=cray"):
            self.spec.mpicc = spack_cc
            self.spec.mpicxx = spack_cxx
            self.spec.mpifc = spack_fc
            self.spec.mpif77 = spack_f77
        else:
            self.spec.mpicc = join_path(self.prefix.bin, "mpicc")
            self.spec.mpicxx = join_path(self.prefix.bin, "mpicxx")
            self.spec.mpifc = join_path(self.prefix.bin, "mpif90")
            self.spec.mpif77 = join_path(self.prefix.bin, "mpif77")

        self.spec.mpicxx_shared_libs = [
            os.path.join(self.prefix.lib, "libmpicxx.{0}".format(dso_suffix)),
            os.path.join(self.prefix.lib, "libmpi.{0}".format(dso_suffix)),
        ]

    @run_before("configure")
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError("Mvapich requires both C and Fortran compilers!")

    def configure_args(self):
        spec = self.spec
        args = [
            "--disable-silent-rules",
            "--disable-new-dtags",
            "--disable-cl",
            "--disable-opencl",
            "--disable-gl",
            "--enable-fortran=all",
            "-disable-omb",
            "--enable-wrapper-rpath={0}".format("no" if "~wrapperrpath" in spec else "yes"),
        ]

        args.extend(self.enable_or_disable("alloca"))
        #args.append("--with-pmi=" + spec.variants["pmi_version"].value)

        if "+debug" in self.spec:
            args.extend(
                [
                    "--disable-fast",
                    "--enable-error-checking=runtime",
                    "--enable-error-messages=all",
                    # Permits debugging with TotalView
                    "--enable-g=all",
                    "--enable-debuginfo",
                ]
            )
        else:
            args.append("--enable-fast=all")
        if "+cuda" in self.spec:
            gpu_map={"Volta":"70","Ampere":"80","Hopper":"90"}
            args.extend(["--enable-cuda", "--with-cuda={0}".format(spec["cuda"].prefix),'NVCCFLAGS=-gencode=arch=compute_{0},code=sm_{0}'.format(gpu_map[spec.variants['nvidia_arch'].value]),'CFLAGS=-I{0}'.format(spec["cuda"].prefix+"/include"),'CXXFLAGS=-I{0}'.format(spec["cuda"].prefix+"/include")])
        if "+rocm" in self.spec:
            args.extend(["--enable-rocm", "--with-rocm={0}".format(spec["hip"].prefix),"--enable-hip=basic"])

        if "+regcache" in self.spec:
            args.append("--enable-registration-cache")
        else:
            args.append("--disable-registration-cache")


        ld = ""
        for path in itertools.chain(self.compiler.extra_rpaths, self.compiler.implicit_rpaths()):
            ld += "-Wl,-rpath," + path + " "
        if ld != "":
            args.append("LDFLAGS=" + ld)
        args.extend(self.process_manager_options)
        args.extend(self.network_options)
        args.extend(self.file_system_options)
        return args
                                                                                                                                                            
