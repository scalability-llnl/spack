# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import sys

from spack.package import *


class Mvapich2x(AutotoolsPackage):
    """MVAPICH2-X is the advanced version of the MVAPICH2 MPI library with
    enhanced features (UMR, ODP, DC, Core-Direct, SHARP, XPMEM), OSU INAM
    (InifniBand Network Monitoring and Analysis),PGAS (OpenSHMEM, UPC, UPC++,
    and CAF), and MPI+PGAS programming models with unified communication
    runtime. MVAPICH2-X is not installable from source and is only available
    through a binary mirror. If you do not find the binary you're looking for,
    send us an email at mvapich@cse.ohio-state.edu. The binary mirror url is:
    http://mvapich.cse.ohio-state.edu/download/mvapich/spack-mirror/mvapich2x/
    """

    homepage = "https://mvapich.cse.ohio-state.edu"
    url = "http://mvapich.cse.ohio-state.edu/download/mvapich/spack-mirror/mvapich2x/mvapich2x-2.3.tar.gz"

    maintainers("natshineman", "harisubramoni", "ndcontini")

    version(
        "2.3",
        sha256="fc47070e2e9fac09b97022be2320200d732a0a4a820a2b51532b88f8ded14536",
        preferred=True,
    )
    version("2.3rc3", sha256="85a9f1ea1a837d487e356f021ef6f3a4661ad270a0c5f54777b362ee4d45166f")

    provides("mpi")
    provides("mpi@:3.1")

    variant(
        "feature",
        description=(
            "Feature descriptions are specified at: "
            "https://mvapich.cse.ohio-state.edu/downloads/"
        ),
        default="basic",
        values=("basic", "basic-xpmem", "advanced", "advanced-xpmem"),
        multi=False,
    )

    variant(
        "process_managers",
        description="List of the process managers to activate",
        default="mpirun",
        values=("slurm", "mpirun", "pbs", "jsrun"),
        multi=False,
    )

    variant(
        "distribution",
        description="The type of distribution of the fabric.",
        default="stock-ofed",
        values=(
            "stock-ofed",
            "mofed4.5",
            "mofed4.6",
            "mofed4.7",
            "mofed5.0",
            "ifs10.6",
            "ifs10.9",
        ),
        multi=False,
    )

    variant(
        "pmi_version",
        description=(
            "The pmi version to be used with slurm. This variant is "
            "IGNORED if set for mpirun or jsrun. jsrun uses pmix "
            "regardless of chosen option."
        ),
        default="pmi1",
        values=("pmi1", "pmi2", "pmix"),
        multi=False,
    )

    depends_on("bison@3.4.2", type="build")
    depends_on("libpciaccess@0.13.5", when=(sys.platform != "darwin"))
    depends_on("libxml2@2.9.10")
    depends_on("pmix@3.1.3", when="pmi_version=pmix")

    filter_compiler_wrappers("mpicc", "mpicxx", "mpif77", "mpif90", "mpifort", relative_root="bin")

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ["libmpi"]

        if "cxx" in query_parameters:
            libraries = ["libmpicxx"] + libraries

        return find_libraries(libraries, root=self.prefix, shared=True, recursive=True)

    @property
    def process_feature_options(self):
        spec = self.spec
        opts = []

        if "feature=basic" in spec:
            opts = [
                "--enable-mcast",
                "--enable-hybrid",
                "--enable-mpit-tool",
                "--enable-mpit-pvars=mv2",
            ]
        elif "feature=basic-xpmem" in spec:
            opts = [
                "--enable-mcast",
                "--enable-hybrid",
                "--enable-mpit-tool",
                "--enable-mpit-pvars=mv2",
                "--with-xpmem=/opt/xpmem/",
            ]
        elif "feature=advanced" in spec:
            opts = [
                "--enable-mcast",
                "--enable-hybrid",
                "--enable-mpit-tool",
                "--enable-mpit-pvars=mv2",
                "--with-core-direct",
                "--enable-dc",
                "--enable-umr",
            ]
        elif "feature=advanced-xpmem" in spec:
            opts = [
                "--enable-mcast",
                "--enable-hybrid",
                "--enable-mpit-tool",
                "--enable-mpit-pvars=mv2",
                "--with-core-direct",
                "--enable-dc",
                "--enable-umr",
                "--with-xpmem=/opt/xpmem/",
            ]
        return opts

    @property
    def distribution_options(self):
        opts = []
        if "distribution=ifs10.6" in self.spec or "distribution=ifs10.9" in self.spec:
            opts = ["--with-device=ch3:psm"]
        else:
            opts = ["--with-device=ch3:mrail", "--with-rdma=gen2"]
        return opts

    @property
    def process_manager_options(self):
        spec = self.spec
        opts = []
        # See: http://slurm.schedmd.com/mpi_guide.html#mvapich2
        if "process_managers=slurm" in spec:
            opts = ["--with-ch3-rank-bits=32", "--with-pm=slurm"]
            if "pmi_version=pmi1" in spec:
                opts.append("--with-pmi=pmi1")
            if "pmi_version=pmi2" in spec:
                opts.append("--with-pmi=pmi2")
            if "pmi_version=pmix" in spec:
                opts.append("--with-pmi=pmix")
                opts.append("--with-pmix={0}".format(spec["pmix"].prefix))
        elif "process_managers=pbs" in spec:
            opts = ["--with-ch3-rank-bits=32", "--with-pbs=/opt/pbs", "--with-pm=hydra"]
        elif "process_managers=jsrun" in spec:
            opts = [
                "--with-ch3-rank-bits=32",
                "--with-pmi=pmix",
                "--with-pmix={0}".format(["pmix"].prefix),
                "--with-pm=jsm",
            ]
        opts.append("--disable-gl")
        return opts

    @property
    def construct_ldflags(self):
        # LDFLAGS contributed by the process manager
        spec = self.spec
        xpmem_ldflags = ""
        if "feature=basic-xpmem" in spec or "feature=advanced-xpmem" in spec:
            xpmem_ldflags = " -Wl,-rpath,/opt/xpmem/lib " "-L/opt/xpmem/lib -lxpmem"

        # Add default LDFLAGS and combine together
        LDFLAGS = "LDFLAGS=-Wl,-rpath,XORIGIN/placeholder"
        LDFLAGS = LDFLAGS + xpmem_ldflags
        return LDFLAGS

    @property
    def construct_cflags(self):
        # CFLAGS contributed by the feature
        spec = self.spec
        cflags = "CFLAGS="
        if "feature=basic-xpmem" in spec or "feature=advanced-xpmem" in spec:
            cflags = cflags + "-I/opt/xpmem/include"
        return cflags

    def setup_build_environment(self, env):
        # mvapich2 configure fails when F90 and F90FLAGS are set
        env.unset("F90")
        env.unset("F90FLAGS")

    def setup_run_environment(self, env):
        if "pmi_version=pmi1" in self.spec:
            env.set("SLURM_MPI_TYPE", "pmi1")
        if "pmi_version=pmi2" in self.spec:
            env.set("SLURM_MPI_TYPE", "pmi2")
        if "pmi_version=pmix" in self.spec:
            env.set("SLURM_MPI_TYPE", "pmix")

        # Because MPI functions as a compiler, we need to treat it as one and
        # add its compiler paths to the run environment.
        self.setup_compiler_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_compiler_environment(env)
        # use the Spack compiler wrappers under MPI
        dependent_module = dependent_spec.package.module
        env.set("MPICH_CC", dependent_module.spack_cc)
        env.set("MPICH_CXX", dependent_module.spack_cxx)
        env.set("MPICH_F77", dependent_module.spack_f77)
        env.set("MPICH_F90", dependent_module.spack_fc)
        env.set("MPICH_FC", dependent_module.spack_fc)

    def setup_compiler_environment(self, env):
        # For Cray MPIs, the regular compiler wrappers *are* the MPI wrappers.
        # Cray MPIs always have cray in the module name, e.g. "cray-mvapich"
        env.set("MPICC", join_path(self.prefix.bin, "mpicc"))
        env.set("MPICXX", join_path(self.prefix.bin, "mpicxx"))
        env.set("MPIF77", join_path(self.prefix.bin, "mpif77"))
        env.set("MPIF90", join_path(self.prefix.bin, "mpif90"))

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = join_path(self.prefix.bin, "mpicc")
        self.spec.mpicxx = join_path(self.prefix.bin, "mpicxx")
        self.spec.mpifc = join_path(self.prefix.bin, "mpif90")
        self.spec.mpif77 = join_path(self.prefix.bin, "mpif77")
        self.spec.mpicxx_shared_libs = [
            os.path.join(self.prefix.lib, "libmpicxx.{0}".format(dso_suffix)),
            os.path.join(self.prefix.lib, "libmpi.{0}".format(dso_suffix)),
        ]

    def configure_args(self):
        spec = self.spec

        args = [
            "--enable-ucr",
            "--disable-static",
            "--enable-shared",
            "--disable-rdma-cm",
            "--without-hydra-ckpointlib",
        ]
        args.extend(self.process_manager_options)
        args.extend(self.distribution_options)
        args.append(self.construct_cflags)
        args.append(self.construct_ldflags)

        # prevents build error regarding gfortran not allowing mismatched arguments
        if spec.satisfies("%gcc@10.0.0:"):
            args.extend(["FFLAGS=-fallow-argument-mismatch", "FCFLAGS=-fallow-argument-mismatch"])
        return args
