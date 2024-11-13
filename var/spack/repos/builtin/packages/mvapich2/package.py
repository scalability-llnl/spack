# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import re
import sys

from spack.package import *


class Mvapich2(AutotoolsPackage):
    """Mvapich2 is a High-Performance MPI Library for clusters with diverse
    networks (InfiniBand, Omni-Path, Ethernet/iWARP, and RoCE) and computing
    platforms (x86 (Intel and AMD), ARM and OpenPOWER)"""

    homepage = "https://mvapich.cse.ohio-state.edu/userguide/userguide_spack/"
    url = "https://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.3.7.tar.gz"
    list_url = "https://mvapich.cse.ohio-state.edu/downloads/"

    maintainers("natshineman", "harisubramoni", "ndcontini")

    executables = ["^mpiname$", "^mpichversion$"]

    # Prefer the latest stable release
    version("2.3.7-1", sha256="fdd971cf36d6476d007b5d63d19414546ca8a2937b66886f24a1d9ca154634e4")
    version("2.3.7", sha256="c39a4492f4be50df6100785748ba2894e23ce450a94128181d516da5757751ae")
    version("2.3.6", sha256="b3a62f2a05407191b856485f99da05f5e769d6381cd63e2fcb83ee98fc46a249")
    version("2.3.5", sha256="f9f467fec5fc981a89a7beee0374347b10c683023c76880f92a1a0ad4b961a8c")
    version("2.3.4", sha256="7226a45c7c98333c8e5d2888119cce186199b430c13b7b1dca1769909e68ea7a")
    version("2.3.3", sha256="41d3261be57e5bc8aabf4e32981543c015c5443ff032a26f18205985e18c2b73")
    version("2.3.2", sha256="30cc0d7bcaa075d204692f76bca4d65a539e0f661c7460ffa9f835d6249e1ebf")
    version("2.3.1", sha256="314e12829f75f3ed83cd4779a972572d1787aac6543a3d024ea7c6080e0ee3bf")
    version("2.3", sha256="01d5fb592454ddd9ecc17e91c8983b6aea0e7559aa38f410b111c8ef385b50dd")
    version("2.3rc2", sha256="dc3801f879a54358d17002a56afd45186e2e83edc5b8367b5c317e282eb6d6bf")
    version("2.3rc1", sha256="607d309c864a6d57f5fa78fe6dd02368919736b8be0f4ddb938aba303ef9c45c")
    version("2.3a", sha256="7f0bc94265de9f66af567a263b1be6ef01755f7f6aedd25303d640cc4d8b1cff")
    version("2.2", sha256="791a6fc2b23de63b430b3e598bf05b1b25b82ba8bf7e0622fc81ba593b3bb131")
    version("2.1", sha256="49f3225ad17d2f3b6b127236a0abdc979ca8a3efb8d47ab4b6cd4f5252d05d29")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    provides("mpi")
    provides("mpi@:3.1", when="@2.3:")
    provides("mpi@:3.0", when="@2.1:")

    variant("wrapperrpath", default=True, description="Enable wrapper rpath")
    variant("debug", default=False, description="Enable debug info and error messages at run-time")

    variant("cuda", default=False, description="Enable CUDA extension")

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

    # 32 is needed when job size exceeds 32768 cores
    variant(
        "ch3_rank_bits",
        default="32",
        values=("16", "32"),
        multi=False,
        description="Number of bits allocated to the rank field (16 or 32)",
    )

    variant(
        "process_managers",
        description="List of the process managers to activate",
        values=disjoint_sets(("auto",), ("slurm",), ("hydra", "gforker", "remshell"))
        .prohibit_empty_set()
        .with_error("'slurm' or 'auto' cannot be activated along with " "other process managers")
        .with_default("auto")
        .with_non_feature_values("auto"),
    )

    variant(
        "pmi_version",
        description=("The pmi version to be used with slurm"),
        when="process_managers=slurm",
        default="pmi2",
        values=("pmi1", "pmi2", "pmix"),
        multi=False,
    )

    variant(
        "fabrics",
        description="Select the fabric to be enabled for this build."
        "If you have verbs (either from OFED or MOFED), PSM or PSM2 "
        "installed on the system already, you may need to setup external "
        "packages in the package.yaml file for rdma-core, psm or opa-psm2. "
        "This is recommended to avoid unexpected runtime failures. For "
        "more info, visit the homepage url.",
        default="mrail",
        values=(
            "psm",
            "psm2",
            "sock",
            "nemesisib",
            "nemesis",
            "mrail",
            "nemesisibtcp",
            "nemesistcpib",
            "nemesisofi",
        ),
    )

    variant(
        "alloca", default=False, description="Use alloca to allocate temporary memory if available"
    )

    variant("hwlocv2", default=False, description="Builds mvapich2 with hwloc v2")
    variant("hwloc_graphics", default=False, description="Enables hwloc graphics")
    variant(
        "file_systems",
        description="List of the ROMIO file systems to activate",
        values=auto_or_any_combination_of("lustre", "gpfs", "nfs", "ufs"),
    )

    depends_on("automake@1.15", type="build")  # needed for torque patch
    depends_on("findutils", type="build")
    depends_on("bison", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("zlib-api")
    depends_on("libpciaccess", when=(sys.platform != "darwin"))
    depends_on("libxml2")
    depends_on("cuda", when="+cuda")
    depends_on("psm", when="fabrics=psm")
    depends_on("opa-psm2", when="fabrics=psm2")
    depends_on("rdma-core", when="fabrics=mrail")
    depends_on("rdma-core", when="fabrics=nemesisib")
    depends_on("rdma-core", when="fabrics=nemesistcpib")
    depends_on("rdma-core", when="fabrics=nemesisibtcp")
    depends_on("libfabric", when="fabrics=nemesisofi")
    depends_on("slurm", when="process_managers=slurm")
    depends_on("pmix", when="pmi_version=pmix")

    # Fix segmentation fault in `MPIR_Attr_delete_list`:
    # <https://lists.osu.edu/pipermail/mvapich-discuss/2023-January/010695.html>.
    patch("mpir_attr_delete_list_segfault.patch", when="@2.3.7")

    conflicts("fabrics=psm2", when="@:2.1")  # psm2 support was added at version 2.2

    patch("fix-torque.patch", when="@2.3.7-1")

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

    @classmethod
    def determine_variants(cls, exes, version):
        def get_spack_compiler_spec(path):
            spack_compilers = spack.compilers.find_compilers([path])
            for spack_compiler in spack_compilers:
                if os.path.dirname(spack_compiler.cc) == path:
                    return spack_compiler.spec
            return None

        results = []
        for exe in exes:
            variants = ""
            if exe.endswith("mpichversion"):
                output = Executable(exe)(output=str, error=str)
            elif exe.endswith("mpiname"):
                output = Executable(exe)("-a", output=str, error=str)

            if re.search(r"--enable-wrapper-rpath=yes", output):
                variants += "+wrapperrpath"
            else:
                variants += "~wrapperrpath"

            if (
                re.search(r"--disable-fast", output)
                and re.search(r"--enable-error-checking=runtime", output)
                and re.search(r"--enable-error-messages", output)
                and re.search(r"--enable-g", output)
                and re.search(r"--enable-debuginfo", output)
            ):
                variants += "+debug"
            else:
                variants += "~debug"

            if re.search("--enable-cuda", output):
                variants += "+cuda"
            else:
                variants += "~cuda"

            if re.search("--enable-registration-cache", output):
                variants += "+regcache"
            else:
                variants += "~regcache"

            match = re.search(r"--enable-threads=(\S+)", output)
            if match:
                variants += " threads=" + match.group(1)

            match = re.search(r"--with-ch3-rank-bits=(\S+)", output)
            if match:
                variants += " ch3_rank_bits=" + match.group(1)

            pms = []
            if re.search(r"--with-pm=slurm", output):
                pms.append("slurm")
            if re.search(r"--with-pm=[A-Za-z0-9:]*hydra", output):
                pms.append("hydra")
            if re.search(r"--with-pm=[A-Za-z0-9:]*gforker", output):
                pms.append("gforker")
            if re.search(r"--with-pm=[A-Za-z0-9:]*remshell", output):
                pms.append("remshell")
            if pms:
                variants += " process_managers=" + ",".join(pms)

            fabrics = {
                "sock": "ch3:sock",
                "nemesistcpib": "ch3:nemesis:tcp,ib",
                "nemesisibtcp": "ch3:nemesis:ib,tcp",
                "nemesisib": "ch3:nemesis:ib",
                "nemesis": "ch3:nemesis",
                "mrail": "ch3:mrail",
                "nemesisofi": "ch3:nemesis:ofi",
            }
            for fabric_name, conf_flag in fabrics.items():
                if re.search(r"--with-device=" + conf_flag, output):
                    variants += " fabrics=" + fabric_name
                    break
            else:
                if re.search(r"--with-device=psm", output):
                    if re.search(r"--with-psm=", output):
                        variants += " fabrics=psm"
                    elif re.search(r"--with-psm2=", output):
                        variants += " fabrics=psm2"

            used_fs = []
            for fs in ("lustre", "gpfs", "nfs", "ufs"):
                if re.search("--with-file-system=[a-zA-Z0-9+]*" + fs, output):
                    used_fs.append(fs)
            if used_fs:
                variants += " file_systems=" + ",".join(used_fs)

            match = re.search(r"CC: (\S+)", output)
            if match:
                comp_spec = get_spack_compiler_spec(os.path.dirname(match.group(1)))
                if comp_spec:
                    variants += " %" + str(comp_spec)
            results.append(variants)
        return results

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
            opts = ["--with-pm=slurm", "--with-slurm={0}".format(spec["slurm"].prefix)]
            if "pmi_version=pmi1" in spec:
                opts.append("--with-pmi=pmi1")
            elif "pmi_version=pmi2" in spec:
                opts.append("--with-pmi=pmi2")
            elif "pmi_version=pmix" in spec:
                opts.append("--with-pmi=pmix")
                opts.append("--with-pmix={0}".format(spec["pmix"].prefix))

        return opts

    @property
    def network_options(self):
        opts = []
        # From here on I can suppose that only one variant has been selected
        if "fabrics=psm" in self.spec:
            opts = ["--with-device=ch3:psm", "--with-psm={0}".format(self.spec["psm"].prefix)]
        elif "fabrics=psm2" in self.spec:
            opts = [
                "--with-device=ch3:psm",
                "--with-psm2={0}".format(self.spec["opa-psm2"].prefix),
            ]
        elif "fabrics=sock" in self.spec:
            opts = ["--with-device=ch3:sock"]
        elif "fabrics=nemesistcpib" in self.spec:
            opts = ["--with-device=ch3:nemesis:tcp,ib"]
        elif "fabrics=nemesisibtcp" in self.spec:
            opts = ["--with-device=ch3:nemesis:ib,tcp"]
        elif "fabrics=nemesisib" in self.spec:
            opts = ["--with-device=ch3:nemesis:ib"]
        elif "fabrics=nemesis" in self.spec:
            opts = ["--with-device=ch3:nemesis"]
        elif "fabrics=mrail" in self.spec:
            opts = ["--with-device=ch3:mrail", "--with-rdma=gen2", "--disable-mcast"]
        elif "fabrics=nemesisofi" in self.spec:
            opts = [
                "--with-device=ch3:nemesis:ofi",
                "--with-ofi={0}".format(self.spec["libfabric"].prefix),
            ]
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

    def setup_run_environment(self, env):
        if "process_managers=slurm" in self.spec:
            if "pmi_version=pmi1" in self.spec:
                env.set("SLURM_MPI_TYPE", "pmi1")
            elif "pmi_version=pmi2" in self.spec:
                env.set("SLURM_MPI_TYPE", "pmi2")
            elif "pmi_version=pmix" in self.spec:
                env.set("SLURM_MPI_TYPE", "pmix")

        env.set("MPI_ROOT", self.prefix)

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

    @run_before("configure")
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError("Mvapich2 requires both C and Fortran compilers!")

    def configure_args(self):
        spec = self.spec
        args = [
            "--enable-shared",
            "--enable-romio",
            "--disable-silent-rules",
            "--disable-new-dtags",
            "--enable-fortran=all",
            "--enable-threads={0}".format(spec.variants["threads"].value),
            "--with-ch3-rank-bits={0}".format(spec.variants["ch3_rank_bits"].value),
            "--enable-wrapper-rpath={0}".format("no" if "~wrapperrpath" in spec else "yes"),
        ]

        args.extend(self.enable_or_disable("alloca"))

        if "+debug" in self.spec:
            args.extend(
                [
                    "--disable-fast",
                    "--enable-error-checking=runtime",
                    "--enable-error-messages=all",
                    # Permits debugging with TotalView
                    "--enable-g=dbg",
                    "--enable-debuginfo",
                ]
            )
        else:
            args.append("--enable-fast=all")

        if "+cuda" in self.spec:
            args.extend(["--enable-cuda", "--with-cuda={0}".format(spec["cuda"].prefix)])
        else:
            args.append("--disable-cuda")
        if "~hwloc_graphics" in self.spec:
            args.append("--disable-opencl")
            args.append("--disable-gl")
            args.append("--disable-nvml")
        if "+hwlocv2" in self.spec:
            args.append("--with-hwloc=v2")
        if "+regcache" in self.spec:
            args.append("--enable-registration-cache")
        else:
            args.append("--disable-registration-cache")

        args.extend(self.process_manager_options)
        args.extend(self.network_options)
        args.extend(self.file_system_options)
        return args
