# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

from spack.build_environment import dso_suffix
from spack.package import *


class Mpich(AutotoolsPackage, CudaPackage, ROCmPackage):
    """MPICH is a high performance and widely portable implementation of
    the Message Passing Interface (MPI) standard."""

    homepage = "https://www.mpich.org"
    url = "https://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
    git = "https://github.com/pmodels/mpich.git"
    list_url = "https://www.mpich.org/static/downloads/"
    list_depth = 1

    maintainers("raffenet", "yfguo")
    tags = ["e4s"]
    executables = ["^mpichversion$"]

    keep_werror = "specific"

    license("mpich2")

    version("develop", submodules=True)
    version("4.2.3", sha256="7a019180c51d1738ad9c5d8d452314de65e828ee240bcb2d1f80de9a65be88a8")
    version("4.2.2", sha256="883f5bb3aeabf627cb8492ca02a03b191d09836bbe0f599d8508351179781d41")
    version("4.2.1", sha256="23331b2299f287c3419727edc2df8922d7e7abbb9fd0ac74e03b9966f9ad42d7")
    version("4.2.0", sha256="a64a66781b9e5312ad052d32689e23252f745b27ee8818ac2ac0c8209bc0b90e")
    version("4.1.2", sha256="3492e98adab62b597ef0d292fb2459b6123bc80070a8aa0a30be6962075a12f0")
    version("4.1.1", sha256="ee30471b35ef87f4c88f871a5e2ad3811cd9c4df32fd4f138443072ff4284ca2")
    version("4.1", sha256="8b1ec63bc44c7caa2afbb457bc5b3cd4a70dbe46baba700123d67c48dc5ab6a0")
    version("4.0.3", sha256="17406ea90a6ed4ecd5be39c9ddcbfac9343e6ab4f77ac4e8c5ebe4a3e3b6c501")
    version("4.0.2", sha256="5a42f1a889d4a2d996c26e48cbf9c595cbf4316c6814f7c181e3320d21dedd42")
    version("4.0.1", sha256="66a1fe8052734af2eb52f47808c4dfef4010ceac461cb93c42b99acfb1a43687")
    version("4.0", sha256="df7419c96e2a943959f7ff4dc87e606844e736e30135716971aba58524fbff64")
    version("3.4.3", sha256="8154d89f3051903181018166678018155f4c2b6f04a9bb6fe9515656452c4fd7")
    version("3.4.2", sha256="5c19bea8b84e8d74cca5f047e82b147ff3fba096144270e3911ad623d6c587bf")
    version("3.4.1", sha256="8836939804ef6d492bcee7d54abafd6477d2beca247157d92688654d13779727")
    version("3.4", sha256="ce5e238f0c3c13ab94a64936060cff9964225e3af99df1ea11b130f20036c24b")
    version("3.3.2", sha256="4bfaf8837a54771d3e4922c84071ef80ffebddbb6971a006038d91ee7ef959b9")
    version("3.3.1", sha256="fe551ef29c8eea8978f679484441ed8bb1d943f6ad25b63c235d4b9243d551e5")
    version("3.3", sha256="329ee02fe6c3d101b6b30a7b6fb97ddf6e82b28844306771fa9dd8845108fa0b")
    version("3.2.1", sha256="5db53bf2edfaa2238eb6a0a5bc3d2c2ccbfbb1badd79b664a1a919d2ce2330f1")
    version("3.2", sha256="0778679a6b693d7b7caff37ff9d2856dc2bfc51318bf8373859bfa74253da3dc")
    version("3.1.4", sha256="f68b5330e94306c00ca5a1c0e8e275c7f53517d01d6c524d51ce9359d240466b")
    version("3.1.3", sha256="afb690aa828467721e9d9ab233fe00c68cae2b7b930d744cb5f7f3eb08c8602c")
    version("3.1.2", sha256="37c3ba2d3cd3f4ea239497d9d34bd57a663a34e2ea25099c2cbef118c9156587")
    version("3.1.1", sha256="455ccfaf4ec724d2cf5d8bff1f3d26a958ad196121e7ea26504fd3018757652d")
    version("3.1", sha256="fcf96dbddb504a64d33833dc455be3dda1e71c7b3df411dfcf9df066d7c32c39")
    version("3.0.4", sha256="cf638c85660300af48b6f776e5ecd35b5378d5905ec5d34c3da7a27da0acf0b3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("hwloc", default=True, description="Use external hwloc package")
    variant("hydra", default=True, description="Build the hydra process manager")
    variant("romio", default=True, description="Enable ROMIO MPI I/O implementation")
    variant("verbs", default=False, description="Build support for OpenFabrics verbs.")
    variant("slurm", default=False, description="Enable Slurm support")
    variant("wrapperrpath", default=True, description="Enable wrapper rpath")
    variant(
        "pmi",
        default="default",
        description="""PMI interface.""",
        values=("default", "pmi", "pmi2", "pmix", "cray"),
        multi=False,
    )
    variant(
        "device",
        default="ch4",
        description="""Abstract Device Interface (ADI)
implementation. The ch4 device is in experimental state for versions
before 3.4.""",
        values=("ch3", "ch4", "ch3:sock"),
        multi=False,
    )
    variant(
        "netmod",
        default="ofi",
        description="""Network module. Only single netmod builds are
supported, and netmod is ignored if device is ch3:sock.""",
        values=("tcp", "mxm", "ofi", "ucx"),
        multi=False,
    )
    variant(
        "pci",
        default=(sys.platform != "darwin"),
        description="Support analyzing devices on PCI bus",
    )
    variant(
        "libxml2",
        default=True,
        description="Use libxml2 for XML support instead of the custom "
        "minimalistic implementation",
    )
    variant("argobots", default=False, description="Enable Argobots support")
    variant("fortran", default=True, description="Enable Fortran support")

    variant(
        "vci",
        default=False,
        when="@4: device=ch4",
        description="Enable multiple VCI (virtual communication "
        "interface) critical sections to improve performance "
        "of applications that do heavy concurrent MPI"
        "communications. Set MPIR_CVAR_CH4_NUM_VCIS=<N> to "
        "enable multiple vcis at runtime.",
    )

    variant(
        "datatype-engine",
        default="auto",
        description="controls the datatype engine to use",
        values=("dataloop", "yaksa", "auto"),
        when="@3.4:",
        multi=False,
    )
    for _yaksa_cond in (
        "@4.0: device=ch4 datatype-engine=auto",
        "@4.0: device=ch4 datatype-engine=yaksa",
    ):
        with when(_yaksa_cond):
            depends_on("yaksa")
            depends_on("yaksa+cuda", when="+cuda")
            depends_on("yaksa+rocm", when="+rocm")

    conflicts("datatype-engine=yaksa", when="device=ch3")
    conflicts("datatype-engine=yaksa", when="device=ch3:sock")
    conflicts("datatype-engine=dataloop", when="+cuda")
    conflicts("datatype-engine=dataloop", when="+rocm")

    variant(
        "hcoll",
        default=False,
        description="Enable support for Mellanox HCOLL accelerated "
        "collective operations library",
        when="@3.3: device=ch4 netmod=ucx",
    )
    depends_on("hcoll", when="+hcoll")

    variant("xpmem", default=False, when="@3.4:", description="Enable XPMEM support")
    depends_on("xpmem", when="+xpmem")

    # Todo: cuda can be a conditional variant, but it does not seem to work when
    # overriding the variant from CudaPackage.
    conflicts("+cuda", when="@:3.3")
    conflicts("+cuda", when="device=ch3")
    conflicts("+cuda", when="device=ch3:sock")
    conflicts("+rocm", when="@:4.0")
    conflicts("+rocm", when="device=ch3")
    conflicts("+rocm", when="device=ch3:sock")
    conflicts("+cuda", when="+rocm", msg="CUDA must be disabled to support ROCm")

    provides("mpi@:4.0")
    provides("mpi@:3.1", when="@:3.2")
    provides("mpi@:3.0", when="@:3.1")
    provides("mpi@:2.2", when="@:1.2")
    provides("mpi@:2.1", when="@:1.1")
    provides("mpi@:2.0", when="@:1.0")

    filter_compiler_wrappers("mpicc", "mpicxx", "mpif77", "mpif90", "mpifort", relative_root="bin")

    # Set correct rpath flags for Intel Fortran Compiler (%oneapi)
    # See https://github.com/pmodels/mpich/pull/5824
    # and https://github.com/spack/spack/issues/31678
    # We do not fetch the patch from the upstream repo because it cannot be applied to older
    # versions.
    with when("%oneapi"):
        patch("mpich-oneapi-config-rpath/step1.patch", when="@:4.0.2")
        patch("mpich-oneapi-config-rpath/step2.patch", when="@3.1.1:4.0.2")

    # Fix using an external hwloc
    # See https://github.com/pmodels/mpich/issues/4038
    # and https://github.com/pmodels/mpich/pull/3540
    # landed in v3.4b1 v3.4a3
    patch(
        "https://github.com/pmodels/mpich/commit/8a851b317ee57366cd15f4f28842063d8eff4483.patch?full_index=1",
        sha256="d2dafc020941d2d8cab82bc1047e4a6a6d97736b62b06e2831d536de1ac01fd0",
        when="@3.3 +hwloc",
    )

    # fix MPI_Barrier segmentation fault
    # see https://lists.mpich.org/pipermail/discuss/2016-May/004764.html
    # and https://lists.mpich.org/pipermail/discuss/2016-June/004768.html
    patch("mpich32_clang.patch", when="@=3.2%clang")
    patch("mpich32_clang.patch", when="@=3.2%apple-clang")

    # Fix SLURM node list parsing
    # See https://github.com/pmodels/mpich/issues/3572
    # and https://github.com/pmodels/mpich/pull/3578
    patch(
        "https://github.com/pmodels/mpich/commit/b324d2de860a7a2848dc38aefb8c7627a72d2003.patch?full_index=1",
        sha256="5f48d2dd8cc9f681cf710b864f0d9b00c599f573a75b1e1391de0a3d697eba2d",
        when="@=3.3",
    )

    # Fix SLURM hostlist_t usage
    # See https://github.com/pmodels/mpich/issues/6806
    # and https://github.com/pmodels/mpich/pull/6820
    patch(
        "https://github.com/pmodels/mpich/commit/7a28682a805acfe84a4ea7b41cea079696407398.patch?full_index=1",
        sha256="8cc80a8ffc3f1c907b1d8176129a0c1d01794a95adbed5b5357f50c13f6560e4",
        when="@4.1:4.1.2 +slurm ^slurm@23-11-1-1:",
    )
    # backports of fix down to v3.3
    patch(
        "mpich40_slurm_hostlist.patch",
        sha256="39aa1353305b7b03bc5c645c87d5299bd5d2ff676750898ba925f6cb9b716bdb",
        when="@4.0 +slurm ^slurm@23-11-1-1:",
    )
    patch(
        "mpich33_slurm_hostlist.patch",
        sha256="d6ec26adcf2d08d0739be44ab65b928a7a88e9ff1375138a0593678eedd420ab",
        when="@3.3:3.4 +slurm ^slurm@23-11-1-1:",
    )

    # Fix reduce operations for unsigned integers
    # See https://github.com/pmodels/mpich/issues/6083
    patch(
        "https://github.com/pmodels/mpich/commit/3a1f618e017547c9710ab4fb01ae258a01477190.patch?full_index=1",
        sha256="d4c0e99a80f6cb0cb0ced91f6ad5da776c4a70f70f805f08096939ec9a92483e",
        when="@4.0:4.0.2",
    )

    # Fix checking whether the datatype is contiguous
    # https://github.com/pmodels/yaksa/pull/189
    # https://github.com/pmodels/mpich/issues/5391
    # The problem has been fixed starting version 4.0 by updating the yaksa git submodule, which
    # has not been done for the 3.4.x branch. The following patch is a backport of the
    # aforementioned pull request for the unreleased version of yaksa that is vendored with MPICH.
    # Note that Spack builds MPICH against a non-vendored yaksa only starting version 4.0.
    with when("@3.4"):
        # Apply the patch only when yaksa is used:
        patch("mpich34_yaksa_hindexed.patch", when="datatype-engine=yaksa")
        patch("mpich34_yaksa_hindexed.patch", when="datatype-engine=auto device=ch4")

    # Fix false positive result of the configure time check for CFI support
    # https://github.com/pmodels/mpich/pull/6537
    # https://github.com/pmodels/mpich/issues/6505
    with when("@3.2.2:4.1.1"):
        # Apply the patch from the upstream repo in case we have to run the autoreconf stage:
        patch(
            "https://github.com/pmodels/mpich/commit/d901a0b731035297dd6598888c49322e2a05a4e0.patch?full_index=1",
            sha256="de0de41ec42ac5f259ea02f195eea56fba84d72b0b649a44c947eab6632995ab",
        )
        # Apply the changes to the configure script to skip the autoreconf stage if possible:
        patch("mpich32_411_CFI_configure.patch")

    depends_on("findutils", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("hwloc@2.0.0:", when="@3.3: +hwloc")

    depends_on("libfabric", when="netmod=ofi")
    depends_on("libfabric fabrics=gni", when="netmod=ofi pmi=cray")
    # The ch3 ofi netmod results in crashes with libfabric 1.7
    # See https://github.com/pmodels/mpich/issues/3665
    depends_on("libfabric@:1.6", when="device=ch3 netmod=ofi")
    depends_on("libfabric@1.5:", when="@3.4: device=ch4 netmod=ofi")

    depends_on("ucx", when="netmod=ucx")
    depends_on("mxm", when="netmod=mxm")

    # The dependencies on libpciaccess and libxml2 come from the embedded
    # hwloc, which, before version 3.3, was used only for Hydra.
    depends_on("libpciaccess", when="@:3.2+hydra+pci")
    depends_on("libxml2", when="@:3.2+hydra+libxml2")

    # Starting with version 3.3, MPICH uses hwloc directly.
    depends_on("libpciaccess", when="@3.3:+pci")
    depends_on("libxml2", when="@3.3:+libxml2")

    # Starting with version 3.3, Hydra can use libslurm for nodelist parsing
    depends_on("slurm", when="+slurm")

    depends_on("pmix", when="pmi=pmix")

    # +argobots variant requires Argobots
    depends_on("argobots", when="+argobots")

    # building from git requires regenerating autotools files
    depends_on("automake@1.15:", when="@develop", type="build")
    depends_on("libtool@2.4.4:", when="@develop", type="build")
    depends_on("m4", when="@develop", type="build")
    depends_on("autoconf@2.67:", when="@develop", type="build")

    # building with "+hwloc' also requires regenerating autotools files
    depends_on("automake@1.15:", when="@3.3 +hwloc", type="build")
    depends_on("libtool@2.4.4:", when="@3.3 +hwloc", type="build")
    depends_on("m4", when="@3.3 +hwloc", type="build")
    depends_on("autoconf@2.67:", when="@3.3 +hwloc", type="build")

    # MPICH's Yaksa submodule requires python to configure
    depends_on("python@3.0:", when="@develop", type="build")

    depends_on("cray-pmi", when="pmi=cray")

    conflicts("device=ch4", when="@:3.2")
    conflicts("netmod=ofi", when="@:3.1.4")
    conflicts("netmod=ucx", when="device=ch3")
    conflicts("netmod=mxm", when="device=ch4")
    conflicts("netmod=mxm", when="@:3.1.3")
    conflicts("netmod=tcp", when="device=ch4")
    conflicts("pmi=pmi2", when="device=ch3 netmod=ofi")
    conflicts("pmi=pmix", when="device=ch3")
    conflicts("pmi=pmix", when="device=ch3:sock")
    conflicts("pmi=pmix", when="+hydra")
    conflicts("pmi=cray", when="+hydra")

    # MPICH does not require libxml2 and libpciaccess for versions before 3.3
    # when ~hydra is set: prevent users from setting +libxml2 and +pci in this
    # case to avoid generating an identical MPICH installation.
    conflicts("+pci", when="@:3.2~hydra")
    conflicts("+libxml2", when="@:3.2~hydra")

    # see https://github.com/pmodels/mpich/pull/5031
    conflicts("%clang@:7", when="@3.4:3.4.1")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)(output=str, error=str)
        match = re.search(r"MPICH Version:\s+(\S+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        def get_spack_compiler_spec(compiler):
            spack_compilers = spack.compilers.find_compilers([os.path.dirname(compiler)])
            actual_compiler = None
            # check if the compiler actually matches the one we want
            for spack_compiler in spack_compilers:
                if spack_compiler.cc and spack_compiler.cc == compiler:
                    actual_compiler = spack_compiler
                    break
            return actual_compiler.spec if actual_compiler else None

        def is_enabled(text):
            if text in set(["t", "true", "enabled", "enable", "with", "yes", "1"]):
                return True
            return False

        def is_disabled(text):
            if text in set(["f", "false", "disabled", "disable", "without", "no", "0"]):
                return True
            return False

        results = []
        for exe in exes:
            variants = []
            output = Executable(exe)(output=str, error=str)
            if re.search(r"--with-hwloc(-prefix)*=embedded", output):
                variants.append("~hwloc")

            if re.search(r"--with-pm=hydra", output):
                variants.append("+hydra")
            else:
                variants.append("~hydra")

            match = re.search(r"--(\S+)-romio", output)
            if match and is_enabled(match.group(1)):
                variants.append("+romio")
            elif match and is_disabled(match.group(1)):
                variants.append("~romio")

            if re.search(r"--with-ibverbs", output):
                variants.append("+verbs")
            elif re.search(r"--without-ibverbs", output):
                variants.append("~verbs")

            match = re.search(r"--enable-wrapper-rpath=(\S+)", output)
            if match and is_enabled(match.group(1)):
                variants.append("+wrapperrpath")
            match = re.search(r"--enable-wrapper-rpath=(\S+)", output)
            if match and is_disabled(match.group(1)):
                variants.append("~wrapperrpath")

            if re.search(r"--disable-fortran", output):
                variants.append("~fortran")

            match = re.search(r"--with-slurm=(\S+)", output)
            if match and is_enabled(match.group(1)):
                variants.append("+slurm")

            if re.search(r"--enable-libxml2", output):
                variants.append("+libxml2")
            elif re.search(r"--disable-libxml2", output):
                variants.append("~libxml2")

            if re.search(r"--with-thread-package=argobots", output):
                variants.append("+argobots")

            if re.search(r"--with-pmi=default", output):
                variants.append("pmi=default")
            elif re.search(r"--with-pmi=simple", output):
                variants.append("pmi=pmi")
            elif re.search(r"--with-pmi=pmi2/simple", output):
                variants.append("pmi=pmi2")
            elif re.search(r"--with-pmi=pmi", output):
                variants.append("pmi=pmi")
            elif re.search(r"--with-pmi=pmi2", output):
                variants.append("pmi=pmi2")
            elif re.search(r"--with-pmix", output):
                variants.append("pmi=pmix")

            match = re.search(r"MPICH Device:\s+(ch3|ch4)", output)
            if match:
                variants.append("device=" + match.group(1))

            match = re.search(r"--with-device=ch.\S+(ucx|ofi|mxm|tcp)", output)
            if match:
                variants.append("netmod=" + match.group(1))

            if re.search(r"--with-hcoll", output):
                variants += "+hcoll"

            match = re.search(r"MPICH CC:\s+(\S+)", output)
            if match:
                compiler = match.group(1)
                compiler_spec = get_spack_compiler_spec(compiler)
                if compiler_spec:
                    variants.append("%" + str(compiler_spec))
            results.append(" ".join(variants))
        return results

    def flag_handler(self, name, flags):
        if name == "fflags":
            # https://bugzilla.redhat.com/show_bug.cgi?id=1795817
            # https://github.com/spack/spack/issues/17934
            # TODO: we should add the flag depending on the real Fortran compiler spec and not the
            #  toolchain spec, which might be mixed.
            if any(self.spec.satisfies(s) for s in ["%gcc@10:", "%apple-clang@11:", "%clang@11:"]):
                # Note that the flag is not needed to build the package starting version 4.1
                # (see https://github.com/pmodels/mpich/pull/5840) but we keep adding the flag here
                # to avoid its presence in the MPI compiler wrappers.
                flags.append("-fallow-argument-mismatch")

        return flags, None, None

    def setup_build_environment(self, env):
        env.unset("F90")
        env.unset("F90FLAGS")

        if "pmi=cray" in self.spec:
            env.set("CRAY_PMI_INCLUDE_OPTS", "-I" + self.spec["cray-pmi"].headers.directories[0])
            env.set("CRAY_PMI_POST_LINK_OPTS", "-L" + self.spec["cray-pmi"].libs.directories[0])

    def setup_run_environment(self, env):
        # Because MPI implementations provide compilers, they have to add to
        # their run environments the code to make the compilers available.
        env.set("MPICC", join_path(self.prefix.bin, "mpicc"))
        env.set("MPICXX", join_path(self.prefix.bin, "mpic++"))
        env.set("MPIF77", join_path(self.prefix.bin, "mpif77"))
        env.set("MPIF90", join_path(self.prefix.bin, "mpif90"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        dependent_module = dependent_spec.package.module
        env.set("MPICH_CC", dependent_module.spack_cc)
        env.set("MPICH_CXX", dependent_module.spack_cxx)
        env.set("MPICH_F77", dependent_module.spack_f77)
        env.set("MPICH_F90", dependent_module.spack_fc)
        env.set("MPICH_FC", dependent_module.spack_fc)

    def setup_dependent_package(self, module, dependent_spec):
        spec = self.spec

        spec.mpicc = join_path(self.prefix.bin, "mpicc")
        spec.mpicxx = join_path(self.prefix.bin, "mpic++")

        if "+fortran" in spec:
            spec.mpifc = join_path(self.prefix.bin, "mpif90")
            spec.mpif77 = join_path(self.prefix.bin, "mpif77")

        spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, "libmpicxx.{0}".format(dso_suffix)),
            join_path(self.prefix.lib, "libmpi.{0}".format(dso_suffix)),
        ]

    def autoreconf(self, spec, prefix):
        """Not needed usually, configure should be already there"""
        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path) and not spec.satisfies("@3.3 +hwloc"):
            return
        # Else bootstrap with autotools
        bash = which("bash")
        bash("./autogen.sh")

    @run_before("autoreconf")
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        # The user can work around this by disabling Fortran explicitly
        # with ~fortran

        f77 = self.compiler.f77
        fc = self.compiler.fc

        fortran_missing = f77 is None or fc is None

        if "+fortran" in self.spec and fortran_missing:
            raise InstallError(
                "mpich +fortran requires Fortran compilers. Configure "
                "Fortran compiler or disable Fortran support with ~fortran"
            )

    def configure_args(self):
        spec = self.spec
        config_args = [
            "--disable-maintainer-mode",
            "--disable-silent-rules",
            "--enable-shared",
            "--with-pm={0}".format("hydra" if "+hydra" in spec else "no"),
            "--{0}-romio".format("enable" if "+romio" in spec else "disable"),
            "--{0}-ibverbs".format("with" if "+verbs" in spec else "without"),
            "--enable-wrapper-rpath={0}".format("no" if "~wrapperrpath" in spec else "yes"),
            "--with-yaksa={0}".format(spec["yaksa"].prefix if "^yaksa" in spec else "embedded"),
        ]

        # see https://github.com/pmodels/mpich/issues/5530
        if spec.platform == "darwin":
            config_args.append("--enable-two-level-namespace")

        # hwloc configure option changed in 4.0
        if spec.satisfies("@4.0:"):
            config_args.append(
                "--with-hwloc={0}".format(spec["hwloc"].prefix if "^hwloc" in spec else "embedded")
            )
        else:
            config_args.append(
                "--with-hwloc-prefix={0}".format(
                    spec["hwloc"].prefix if "^hwloc" in spec else "embedded"
                )
            )

        if "~fortran" in spec:
            config_args.append("--disable-fortran")

        if "+slurm" in spec:
            config_args.append("--with-slurm=yes")
            config_args.append("--with-slurm-include={0}".format(spec["slurm"].prefix.include))
            config_args.append("--with-slurm-lib={0}".format(spec["slurm"].prefix.lib))
        else:
            config_args.append("--with-slurm=no")

        # PMI options changed in 4.2.0
        if spec.satisfies("@4.2:"):
            # default (no option) is to build both PMIv1 and PMI2 client interfaces
            if "pmi=pmi" in spec:
                # make PMI1 the default client interface
                config_args.append("--with-pmi=pmi")
            elif "pmi=pmi2" in spec:
                # make PMI2 the default client interface
                config_args.append("--with-pmi=pmi2")
            elif "pmi=pmix" in spec:
                # use the PMIx client interface with an external PMIx library
                config_args.append("--with-pmi=pmix")
                config_args.append(f"--with-pmix={spec['pmix'].prefix}")
            elif "pmi=cray" in spec:
                # use PMI2 interface of the Cray PMI library
                config_args.append("--with-pmi=pmi2")
                config_args.append(f"--with-pmi2={spec['cray-pmi'].prefix}")
        else:
            if "pmi=pmi" in spec:
                config_args.append("--with-pmi=simple")
            elif "pmi=pmi2" in spec:
                config_args.append("--with-pmi=pmi2/simple")
            elif "pmi=pmix" in spec:
                config_args.append(f"--with-pmix={spec['pmix'].prefix}")
            elif "pmi=cray" in spec:
                config_args.append("--with-pmi=cray")

        if "+cuda" in spec:
            config_args.append("--with-cuda={0}".format(spec["cuda"].prefix))
        elif not spec.satisfies("@3.4:3.4.3"):
            # Versions from 3.4 to 3.4.3 cannot handle --without-cuda
            # (see https://github.com/pmodels/mpich/pull/5060):
            config_args.append("--without-cuda")

        if "+rocm" in spec:
            config_args.append("--with-hip={0}".format(spec["hip"].prefix))
        else:
            config_args.append("--without-hip")

        # setup device configuration
        device_config = ""
        if "device=ch4" in spec:
            device_config = "--with-device=ch4:"
        elif "device=ch3" in spec:
            device_config = "--with-device=ch3:nemesis:"

        # Do not apply any netmod if device is ch3:sock
        if "device=ch3:sock" in spec:
            device_config = "--with-device=ch3:sock"
        elif "netmod=ucx" in spec:
            device_config += "ucx"
        elif "netmod=ofi" in spec:
            device_config += "ofi"
        elif "netmod=mxm" in spec:
            device_config += "mxm"
        elif "netmod=tcp" in spec:
            device_config += "tcp"

        config_args.append(device_config)

        # Specify libfabric or ucx path explicitly, otherwise
        # configure might fall back to an embedded version.
        if "netmod=ofi" in spec:
            config_args.append("--with-libfabric={0}".format(spec["libfabric"].prefix))
        if "netmod=ucx" in spec:
            config_args.append("--with-ucx={0}".format(spec["ucx"].prefix))

        # In other cases the argument is redundant.
        if "@:3.2+hydra" in spec or "@3.3:" in spec:
            # The root configure script passes the argument to the configure
            # scripts of all instances of hwloc (there are three copies of it:
            # for hydra, for hydra2, and for MPICH itself).
            config_args += self.enable_or_disable("libxml2")

        # If +argobots specified, add argobots option
        if "+argobots" in spec:
            config_args.append("--with-thread-package=argobots")
            config_args.append("--with-argobots=" + spec["argobots"].prefix)

        if "+vci" in spec:
            config_args.append("--enable-thread-cs=per-vci")

        if "datatype-engine=yaksa" in spec:
            config_args.append("--with-datatype-engine=yaksa")
        elif "datatype-engine=dataloop" in spec:
            config_args.append("--with-datatype-engine=dataloop")
        elif "datatype-engine=auto" in spec:
            config_args.append("--with-datatype-engine=auto")

        if "+hcoll" in spec:
            config_args.append("--with-hcoll=" + spec["hcoll"].prefix)

        if "+xpmem" in spec:
            config_args.append("--with-xpmem=" + spec["xpmem"].prefix)

        return config_args

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, ["examples", join_path("test", "mpi")])

    def mpi_launcher(self):
        """Determine the appropriate launcher."""
        commands = [
            join_path(self.spec.prefix.bin, "mpirun"),
            join_path(self.spec.prefix.bin, "mpiexec"),
        ]
        if "+slurm" in self.spec:
            commands.insert(0, join_path(self.spec["slurm"].prefix.bin))
        return which(*commands)

    def run_mpich_test(self, subdir, exe, num_procs=1):
        """Compile and run the test program."""
        path = self.test_suite.current_test_cache_dir.join(subdir)
        with working_dir(path):
            src = f"{exe}.c"
            if not os.path.isfile(src):
                raise SkipTest(f"{src} is missing")

            mpicc = which(os.environ["MPICC"])
            mpicc("-Wall", "-g", "-o", exe, src)
            if num_procs > 1:
                launcher = self.mpi_launcher()
                if launcher is not None:
                    launcher("-n", str(num_procs), exe)
                    return

            test_exe = which(exe)
            test_exe()

    def test_cpi(self):
        """build and run cpi"""
        self.run_mpich_test("examples", "cpi")

    def test_finalized(self):
        """build and run finalized"""
        self.run_mpich_test(join_path("test", "mpi", "init"), "finalized")

    def test_manyrma(self):
        """build and run manyrma"""
        self.run_mpich_test(join_path("test", "mpi", "perf"), "manyrma", 2)

    def test_sendrecv(self):
        """build and run sendrecv"""
        self.run_mpich_test(join_path("test", "mpi", "basic"), "sendrecv", 2)
