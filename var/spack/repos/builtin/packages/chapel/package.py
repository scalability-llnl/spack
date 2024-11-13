# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess

import spack.platforms.cray
from spack.package import *
from spack.util.environment import is_system_path, set_env


@llnl.util.lang.memoized
def is_CrayEX():
    # Credit to upcxx package for this hpe-cray-ex detection function
    if spack.platforms.host().name == "linux":
        target = os.environ.get("CRAYPE_NETWORK_TARGET")
        if target in ["ofi", "ucx"]:  # normal case
            return True
        elif target is None:  # but some systems lack Cray PrgEnv
            fi_info = which("fi_info")
            if (
                fi_info
                and fi_info("-l", output=str, error=str, fail_on_error=False).find("cxi") >= 0
            ):
                return True
    return False


class Chapel(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Chapel is a modern programming language that is parallel, productive,
    portable, scalable and open-source. The Chapel package comes with many
    options in the form of variants, most of which can be left unset to allow
    Chapel's built-in scripts to determine the proper values based on the environment."""

    homepage = "https://chapel-lang.org/"

    url = "https://github.com/chapel-lang/chapel/archive/refs/tags/2.2.0.tar.gz"
    git = "https://github.com/chapel-lang/chapel.git"

    test_requires_compiler = True

    # TODO: Re-enable these once we add determine_version and determine_variants
    # executables = ["^chpl$", "^chpldoc$"]

    # A list of GitHub accounts to notify when the package is updated.
    # TODO: add chapel-project github account
    maintainers("arezaii", "bonachea")

    tags = ["e4s"]

    # See https://spdx.org/licenses/ for a list.
    license("Apache-2.0")

    version("main", branch="main")

    version("2.2.0", sha256="9b0ce16ed0b1c777647c3aa852d8d8cacea2c3d8a952548a238f07c0f357a0f9")
    version("2.1.0", sha256="8e164d9a9e705e6b816857e84833b0922ce0bde6a36a9f3a29734830aac168ef")
    version("2.0.1", sha256="47e1f3789478ea870bd4ecdf52acbe469d171b89b663309325431f3da7c75008")
    version("2.0.0", sha256="a8cab99fd034c7b7229be8d4626ec95cf02072646fb148c74b4f48c460c6059c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("fix_spack_cc_wrapper_in_cray_prgenv.patch", when="@2.0.0:")

    launcher_names = (
        "amudprun",
        "aprun",
        "gasnetrun_ibv",
        "gasnetrun_mpi",
        "mpirun4ofi",
        "lsf-gasnetrun_ibv",
        "pals",
        "pbs-aprun",
        "pbs-gasnetrun_ibv",
        "slurm-gasnetrun_ibv",
        "slurm-gasnetrun_mpi",
        "slurm-gasnetrun_ofi",
        "slurm-srun",
        "smp",
        "none",
        "unset",
    )

    # TODO: revise this list of mappings, probably need more logic for cce, see upc++
    compiler_map = {
        "aocc": "clang",
        "apple-clang": "clang",
        "arm": "clang",
        "clang": "clang",
        "cce": "cray-prgenv-cray",
        "dpcpp": "intel",
        "gcc": "gnu",
        "intel": "intel",
        "llvm": "llvm",
        "oneapi": "intel",
        "pgi": "pgi",
        "rocmcc": "clang",
        "unset": "unset",
    }

    cpu_options = (
        "native",
        "none",
        "unknown",
        "unset",
        "aarch64",
        "barcelona",
        "bdver1",
        "bdver2",
        "bdver3",
        "bdver4",
        "broadwell",
        "core2",
        "haswell",
        "ivybridge",
        "k8",
        "k8sse3",
        "nehalem",
        "sandybridge",
        "skylake",
        "thunderx",
        "thunderx2t99",
        "westmere",
    )

    # TODO: add other package dependencies
    package_module_dict = {
        "curl": "curl",
        "hdf5": "hdf5+hl~mpi",
        "libevent": "libevent",
        "protobuf": "py-protobuf",
        "ssl": "openssl",
        "yaml": "libyaml@0.1",
        "zmq": "libzmq",
    }

    platform_opts = (
        "cray-cs",
        "cray-xc",
        "cygwin32",
        "cygwin64",
        "darwin",
        "hpe-apollo",
        "hpe-cray-ex",
        "linux32",
        "linux64",
        "netbsd32",
        "netbsd64",
        "pwr6",
        "unset",
    )

    variant(
        "atomics",
        values=("unset", "cstdlib", "intrinsics", "locks"),
        default="unset",
        description="Select atomics implementation",
        multi=False,
    )

    # TODO: refactor this somehow, this is a separate documentation tool, not a variant of chapel
    variant("chpldoc", default=False, description="Build chpldoc in addition to chpl")

    variant("developer", default=False, description="Enable Chapel developer mode")

    variant(
        "comm",
        default="none",
        description="Build Chapel with multi-locale support",
        values=("gasnet", "none", "ofi", "ugni"),
    )

    variant(
        "comm_substrate",
        default="unset",
        description="Build Chapel with GASNet multi-locale support using the "
        "supplied CHPL_COMM_SUBSTRATE",
        values=("ibv", "ofi", "udp", "smp", "unset"),
        multi=False,
        sticky=True,  # never allow the concretizer to choose this
        when="comm=gasnet",
    )

    variant(
        "pshm",
        default=False,
        description="Build Chapel with fast shared-memory comms between co-locales",
        when="comm=gasnet",
    )

    # Chapel depends on GASNet whenever comm=gasnet.
    # The default (and recommendation) is to use the embedded copy of GASNet.
    # This variant allows overriding with a particular version of GASNet sources,
    # although this is not officially supported and some combinations might be rejected.
    variant(
        "gasnet",
        description="Control the GASNet library version used",
        default="bundled",
        values=("bundled", "spack"),
        multi=False,
        when="comm=gasnet",
    )

    variant(
        "gasnet_segment",
        default="unset",
        description="Build Chapel with multi-locale support using the "
        "supplied CHPL_GASNET_SEGMENT",
        values=("everything", "fast", "large", "unset"),
        multi=False,
        when="comm=gasnet",
    )

    variant(
        "gmp",
        description="Build with gmp support",
        default="spack",
        values=("bundled", "none", "spack"),
        multi=False,
    )

    variant(
        "gpu_mem_strategy",
        description="The memory allocation strategy for GPU data",
        values=("array_on_device", "unified_memory"),
        default="array_on_device",
        multi=False,
    )

    variant(
        "host_arch",
        description="Host architecture of the build machine",
        values=("x86_64", "aarch64", "arm64", "unset"),
        default="unset",
        multi=False,
    )

    variant(
        "host_jemalloc",
        values=("bundled", "none", "spack", "unset"),
        default="unset",
        multi=False,
        description="Selects between no jemalloc, bundled jemalloc, or spack supplied jemalloc",
    )

    variant(
        "host_mem",
        values=("cstdlib", "jemalloc"),
        default="jemalloc",
        description="Memory management layer for the chpl compiler",
        multi=False,
    )

    variant(
        "host_platform",
        description="Host platform",
        default="unset",
        values=platform_opts,
        multi=False,
    )

    variant(
        "hwloc",
        description="Build with hwloc support",
        default="bundled",
        values=(
            "bundled",
            "none",
            # CHPL_HWLOC=system existed back to at least 2017,
            # but it was buggy and unsupported until version 2.1
            conditional("spack", when="@2.1:"),
        ),
        multi=False,
    )

    variant(
        "launcher",
        values=launcher_names,
        default="unset",
        description="Launcher to use for running Chapel programs",
        multi=False,
    )

    variant(
        "lib_pic",
        values=("none", "pic"),
        default="none",
        description="Build position-independent code suitable for shared libraries",
    )

    variant(
        "libfabric",
        default="unset",
        description="Control the libfabric version used for multi-locale communication",
        values=("bundled", "spack", "unset"),
        multi=False,
        when="comm=ofi",
    )

    variant(
        "libfabric",
        default="unset",
        description="Control the libfabric version used for multi-locale communication",
        values=("bundled", "spack", "unset"),
        multi=False,
        when="comm=gasnet comm_substrate=ofi",
    )

    requires(
        "^libfabric" + (" fabrics=cxi" if spack.platforms.cray.slingshot_network() else ""),
        when="libfabric=spack",
        msg="libfabric requires cxi fabric provider on HPE-Cray EX machines",
    )

    variant(
        "llvm",
        default="spack",
        description="LLVM backend type. The 'spack' value can use an external "
        "source of LLVM or let spack build a version if no LLVM installs were "
        "previously detected by 'spack external find'",
        values=("bundled", "none", "spack"),
    )

    variant(
        "re2",
        description="Build with re2 support",
        default="bundled",
        values=("bundled", "none"),
        multi=False,
    )

    variant(
        "target_arch",
        description="Target architecture for cross compilation",
        default="unset",
        values=("x86_64", "aarch64", "arm64", "unset"),
        multi=False,
    )

    variant(
        "target_cpu",
        values=cpu_options,
        description="Indicate that the target executable should be specialized "
        "to the given architecture when using --specialize (and --fast).",
        default="unset",
        multi=False,
    )

    variant(
        "target_platform",
        description="Target platform for cross compilation",
        default="unset",
        values=platform_opts,
        multi=False,
    )

    variant(
        "tasks",
        description="Select tasking layer for intra-locale parallelism",
        default="qthreads",
        values=("fifo", "qthreads"),
        multi=False,
    )

    variant(
        "timers",
        description="Select timers implementation",
        default="unset",
        values=("generic", "unset"),
        multi=False,
    )

    variant(
        "unwind",
        description="Build with unwind library for stack tracing",
        default="none",
        values=("bundled", "none", "spack"),
        multi=False,
    )

    # Add dependencies for package modules
    for variant_name, dep in package_module_dict.items():
        variant(
            variant_name,
            description="Build with support for the Chapel {0} package module".format(
                variant_name
            ),
            default=True,
        )
        depends_on(dep, when="+{0}".format(variant_name), type=("build", "link", "run", "test"))

    # TODO: for CHPL_X_CC and CHPL_X_CXX, can we capture an arbitrary path, possibly
    # with arguments?
    chpl_env_vars = [
        "CHPL_ATOMICS",
        "CHPL_AUX_FILESYS",
        "CHPL_COMM",
        "CHPL_COMM_SUBSTRATE",
        "CHPL_DEVELOPER",
        "CHPL_GASNET_SEGMENT",
        "CHPL_GMP",
        "CHPL_GPU",
        "CHPL_GPU_ARCH",
        "CHPL_GPU_MEM_STRATEGY",
        "CHPL_HOST_ARCH",
        # "CHPL_HOST_CC",
        "CHPL_HOST_COMPILER",
        # "CHPL_HOST_CXX",
        "CHPL_HOST_JEMALLOC",
        "CHPL_HOST_MEM",
        "CHPL_HOST_PLATFORM",
        "CHPL_HWLOC",
        "CHPL_LAUNCHER",
        "CHPL_LIB_PIC",
        "CHPL_LIBFABRIC",
        "CHPL_LLVM",
        "CHPL_LLVM_CONFIG",
        "CHPL_LLVM_SUPPORT",
        "CHPL_LLVM_VERSION",
        "CHPL_LOCALE_MODEL",
        "CHPL_MEM",
        "CHPL_RE2",
        "CHPL_SANITIZE",
        "CHPL_SANITIZE_EXE",
        "CHPL_TARGET_ARCH",
        # "CHPL_TARGET_CC",
        "CHPL_TARGET_COMPILER",
        "CHPL_TARGET_CPU",
        # "CHPL_TARGET_CXX",
        "CHPL_TARGET_PLATFORM",
        "CHPL_TASKS",
        "CHPL_TIMERS",
        "CHPL_UNWIND",
    ]

    conflicts("platform=windows")  # Support for windows is through WSL only

    # Ensure GPU support is Sticky: never allow the concretizer to choose this
    variant("rocm", default=False, sticky=True, description="Enable AMD ROCm GPU support")
    variant("cuda", default=False, sticky=True, description="Enable Nvidia CUDA GPU support")

    conflicts("+rocm", when="+cuda", msg="Chapel must be built with either CUDA or ROCm, not both")
    conflicts("+rocm", when="@:1", msg="ROCm support in spack requires Chapel 2.0.0 or later")
    # Chapel restricts the allowable ROCm versions
    with when("@2:2.1 +rocm"):
        depends_on("hsa-rocr-dev@4:5.4")
        depends_on("hip@4:5.4")
    with when("@2.2: +rocm"):
        depends_on("hsa-rocr-dev@4:5.4,6.0:6.2")
        depends_on("hip@4:5.4,6.0:6.2")
    depends_on("llvm-amdgpu@4:5.4", when="+rocm llvm=spack")
    requires("llvm=bundled", when="+rocm ^hip@6.0:6.2", msg="ROCm 6 support requires llvm=bundled")

    conflicts(
        "comm_substrate=unset",
        when="comm=gasnet",
        msg="comm=gasnet requires you to also set comm_substrate= to the appropriate network",
    )

    conflicts(
        "gasnet_segment=everything",
        when="+pshm",
        msg="gasnet_segment=everything does not support +pshm",
    )

    # comm_substrate=udp gasnet_segment=unset defaults to everything,
    # which is incompatible with +pshm
    requires("gasnet_segment=fast", when="+pshm comm_substrate=udp")

    conflicts(
        "^python@3.12:",
        when="@:2.0",
        msg="Chapel versions prior to 2.1.0 may produce SyntaxWarnings with Python >= 3.12",
    )

    conflicts(
        "host_jemalloc=spack",
        when="platform=linux",
        msg="Only bundled jemalloc may be used on Linux systems, see "
        "https://chapel-lang.org/docs/usingchapel/chplenv.html#chpl-host-jemalloc",
    )

    conflicts(
        "host_jemalloc=bundled",
        when="platform=darwin",
        msg="Only system jemalloc may be used on Darwin (MacOS) systems, see "
        "https://chapel-lang.org/docs/usingchapel/chplenv.html#chpl-host-jemalloc",
    )

    with when("llvm=none"):
        conflicts("+cuda", msg="Cuda support requires building with LLVM")
        conflicts("+rocm", msg="ROCm support requires building with LLVM")

    # Add dependencies

    depends_on("doxygen@1.8.17:", when="+chpldoc")

    # TODO: keep up to date with util/chplenv/chpl_llvm.py
    with when("llvm=spack ~rocm"):
        depends_on("llvm@11:17", when="@:2.0.1")
        depends_on("llvm@11:18", when="@2.1.0:")

    # Based on docs https://chapel-lang.org/docs/technotes/gpu.html#requirements
    depends_on("llvm@16:", when="llvm=spack +cuda ^cuda@12:")
    requires(
        "^llvm targets=all",
        msg="llvm=spack +cuda requires LLVM support the nvptx target",
        when="llvm=spack +cuda",
    )

    # This is because certain systems have binutils installed as a system package
    # but do not include the headers. Spack incorrectly supplies those external
    # packages as proper dependencies for LLVM, but then LLVM will fail to build
    # with an error about missing plugin-api.h
    depends_on("binutils+gold+ld+plugins+headers", when="llvm=bundled")

    depends_on("m4", when="gmp=bundled")

    # Runtime dependencies:
    # Note here "run" is run of the Chapel compiler built by this package,
    # but many of these are ALSO run-time dependencies of the executable
    # application built by that Chapel compiler from user-provided sources.
    with default_args(type=("build", "link", "run", "test")):
        depends_on("cuda@11:", when="+cuda")
        depends_on("gmp", when="gmp=spack")
        depends_on("hwloc", when="hwloc=spack")
        depends_on("libfabric", when="libfabric=spack")
        depends_on("libunwind", when="unwind=spack")
        depends_on("jemalloc", when="host_jemalloc=spack")

    depends_on("gasnet conduits=none", when="gasnet=spack")
    depends_on("gasnet@2024.5.0: conduits=none", when="@2.1.0: gasnet=spack")

    depends_on("python@3.7:")
    depends_on("cmake@3.16:")

    # ensure we can map the spack compiler name to one of the ones we recognize
    requires(
        "%aocc",
        "%apple-clang",
        "%arm",
        "%clang",
        "%cce",
        "%cray-prgenv-cray",
        "%cray-prgenv-gnu",
        "%cray-prgenv-intel",
        "%cray-prgenv-pgi",
        "%dpcpp",
        "%gcc",
        "%intel",
        "%llvm",
        "%oneapi",
        "%pgi",
        "%rocmcc",
        policy="one_of",
    )

    def unset_chpl_env_vars(self, env):
        # Clean the environment from any pre-set CHPL_ variables that affect the build
        for var in self.chpl_env_vars:
            env.unset(var)

    def build(self, spec, prefix):
        make()
        if spec.variants["chpldoc"].value:
            make("chpldoc")

    def setup_chpl_platform(self, env):
        if self.spec.variants["host_platform"].value == "unset":
            if is_CrayEX():
                env.set("CHPL_HOST_PLATFORM", "hpe-cray-ex")

    def setup_chpl_compilers(self, env):
        env.set("CHPL_HOST_COMPILER", self.compiler_map[self.spec.compiler.name])
        if (
            self.spec.satisfies("+rocm")
            or self.spec.satisfies("+cuda")
            or self.spec.satisfies("llvm=spack")
        ):
            env.set("CHPL_TARGET_COMPILER", "llvm")
        else:
            env.set("CHPL_TARGET_COMPILER", self.compiler_map[self.spec.compiler.name])

        # Undo spack compiler wrappers:
        # the C/C++ compilers must work post-install
        if self.spec.satisfies("+rocm llvm=spack"):
            env.set(
                "CHPL_LLVM_CONFIG",
                join_path(self.spec["llvm-amdgpu"].prefix, "bin", "llvm-config"),
            )
            real_cc = join_path(self.spec["llvm-amdgpu"].prefix, "bin", "clang")
            real_cxx = join_path(self.spec["llvm-amdgpu"].prefix, "bin", "clang++")

            # +rocm appears to also require a matching LLVM host compiler to guarantee linkage
            env.set("CHPL_HOST_COMPILER", "llvm")
            env.set("CHPL_HOST_CC", real_cc)
            env.set("CHPL_HOST_CXX", real_cxx)

        elif self.spec.satisfies("llvm=spack"):
            env.set("CHPL_LLVM_CONFIG", join_path(self.spec["llvm"].prefix, "bin", "llvm-config"))
            real_cc = join_path(self.spec["llvm"].prefix, "bin", "clang")
            real_cxx = join_path(self.spec["llvm"].prefix, "bin", "clang++")
        else:
            real_cc = self.compiler.cc
            real_cxx = self.compiler.cxx

        if self.spec.satisfies("llvm=spack") or self.spec.satisfies("llvm=none"):
            env.set("CHPL_TARGET_CC", real_cc)
            env.set("CHPL_TARGET_CXX", real_cxx)

    def setup_chpl_comm(self, env, spec):
        env.set("CHPL_COMM", spec.variants["comm"].value)

        if self.spec.satisfies("+pshm"):
            env.set("CHPL_GASNET_MORE_CFG_OPTIONS", "--enable-pshm")

    @run_before("configure", when="gasnet=spack")
    def setup_gasnet(self):
        dst = join_path(self.stage.source_path, "third-party", "gasnet", "gasnet-src")
        remove_directory_contents(dst)
        os.rmdir(dst)
        symlink(self.spec["gasnet"].prefix.src, dst)

    def setup_if_not_unset(self, env, var, value):
        if value != "unset" and var in self.chpl_env_vars:
            if value == "spack":
                value = "system"
            env.set(var, value)

    def prepend_cpath_include(self, env, prefix):
        if not is_system_path(prefix):
            env.prepend_path("CPATH", prefix.include)

    def update_lib_path(self, env, prefix):
        if not is_system_path(prefix):
            env.prepend_path("LD_LIBRARY_PATH", prefix.lib)
            env.prepend_path("LIBRARY_PATH", prefix.lib)
            if prefix.lib.pkgconfig is not None:
                env.prepend_path("PKG_CONFIG_PATH", prefix.lib.pkgconfig)

    def setup_env_vars(self, env):
        # variants that appear unused by Spack typically correspond directly to
        # a CHPL_<variant> variable which will be used by the Chapel build system
        for v in self.spec.variants.keys():
            self.setup_if_not_unset(env, "CHPL_" + v.upper(), str(self.spec.variants[v].value))
        self.setup_chpl_compilers(env)
        self.setup_chpl_platform(env)

        # TODO: a function to set defaults for things where we removed variants
        # We'll set to GPU later if +rocm or +cuda requested
        env.set("CHPL_LOCALE_MODEL", "flat")

        if self.spec.satisfies("+developer"):
            env.set("CHPL_DEVELOPER", "true")

        if not self.spec.satisfies("llvm=none"):
            # workaround Spack issue #44746:
            # Chapel does not directly utilize lua, but many of its
            # launchers depend on system installs of batch schedulers
            # (notably Slurm on Cray EX) which depend on a system Lua.
            # LLVM includes lua as a dependency, but a barebones lua
            # install lacks many packages provided by a system Lua,
            # which are often required by system services like Slurm.
            # Disable the incomplete Spack lua package directory to
            # allow the system one to function.
            env.unset("LUA_PATH")
            env.unset("LUA_CPATH")

        if self.spec.variants["gmp"].value == "spack":
            # TODO: why must we add to CPATH to find gmp.h
            # TODO: why must we add to LIBRARY_PATH to find lgmp
            self.prepend_cpath_include(env, self.spec["gmp"].prefix)
            self.update_lib_path(env, self.spec["gmp"].prefix)

        if self.spec.variants["hwloc"].value == "spack":
            self.update_lib_path(env, self.spec["hwloc"].prefix)
            # Need this for the test env, where it does not appear automatic:
            env.prepend_path("PKG_CONFIG_PATH", self.spec["libpciaccess"].prefix.lib.pkgconfig)

        # TODO: unwind builds but resulting binaries fail to run, producing linker errors
        if self.spec.variants["unwind"].value == "spack":
            # chapel package would not build without cpath, missing libunwind.h
            self.prepend_cpath_include(env, self.spec["libunwind"].prefix)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["libunwind"].prefix.lib)

        if self.spec.satisfies("+yaml"):
            self.prepend_cpath_include(env, self.spec["libyaml"].prefix)
            # could not compile test/library/packages/Yaml/writeAndParse.chpl without this
            self.update_lib_path(env, self.spec["libyaml"].prefix)

        if self.spec.satisfies("+zmq"):
            self.prepend_cpath_include(env, self.spec["libzmq"].prefix)
            # could not compile test/library/packages/ZMQ/hello.chpl without this
            self.update_lib_path(env, self.spec["libzmq"].prefix)
            env.prepend_path("PKG_CONFIG_PATH", self.spec["libsodium"].prefix.lib.pkgconfig)

        if self.spec.satisfies("+curl"):
            self.prepend_cpath_include(env, self.spec["curl"].prefix)
            # could not compile test/library/packages/Curl/check-http.chpl without this
            self.update_lib_path(env, self.spec["curl"].prefix)

        if self.spec.satisfies("+cuda"):
            # TODO: why must we add to LD_LIBRARY_PATH to find libcudart?
            env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix.lib64)
            env.set("CHPL_CUDA_PATH", self.spec["cuda"].prefix)
            env.set("CHPL_LOCALE_MODEL", "gpu")
            env.set("CHPL_GPU", "nvidia")

        if self.spec.satisfies("+rocm"):
            env.set("CHPL_LOCALE_MODEL", "gpu")
            env.set("CHPL_GPU", "amd")
            env.set("CHPL_GPU_ARCH", self.spec.variants["amdgpu_target"].value[0])
            self.prepend_cpath_include(env, self.spec["hip"].prefix)
            env.set("CHPL_ROCM_PATH", self.spec["hip"].prefix)
            self.update_lib_path(env, self.spec["hip"].prefix)
            self.update_lib_path(env, self.spec["hsa-rocr-dev"].prefix)
        self.setup_chpl_comm(env, self.spec)

    def setup_build_environment(self, env):
        self.unset_chpl_env_vars(env)
        self.setup_env_vars(env)

    def setup_run_environment(self, env):
        self.setup_env_vars(env)
        env.prepend_path(
            "PATH", join_path(self.prefix.share, "chapel", self._output_version_short, "util")
        )

    @property
    @llnl.util.lang.memoized
    def _output_version_long(self):
        if str(self.spec.version).lower() == "main":
            return "2.3.0"
        spec_vers_str = str(self.spec.version.up_to(3))
        return spec_vers_str

    @property
    @llnl.util.lang.memoized
    def _output_version_short(self):
        if str(self.spec.version).lower() == "main":
            return "2.3"
        spec_vers_str = str(self.spec.version.up_to(2))
        return spec_vers_str

    def test_version(self):
        """Perform version checks on selected installed package binaries."""
        expected = f"version {self._output_version_long}"
        exes = ["chpl"]

        if self.spec.satisfies("+chpldoc"):
            exes.append("chpldoc")

        for exe in exes:
            reason = f"ensure version of {exe} is {self._output_version_long}"
            with test_part(self, f"test_version_{exe}", purpose=reason):
                path = join_path(self.prefix.bin, exe)
                if not os.path.isfile(path):
                    raise SkipTest(f"{path} is not installed")
                prog = which(path)
                if prog is None:
                    raise RuntimeError(f"Could not find {path}")
                output = prog("--version", output=str.split, error=str.split)
                assert expected in output

    def check(self):
        # TODO: we skip the self-check because it's ran by default but:
        #       - make check doesn't work at build time b/c the PATH isn't yet updated
        #       - make test is a long running operation
        pass

    def check_chpl_install_gasnet(self):
        """Setup env to run self-test after installing the package with gasnet"""
        with set_env(
            GASNET_SPAWNFN="L",
            GASNET_QUIET="yes",
            GASNET_ROUTE_OUTPUT="0",
            QT_AFFINITY="no",
            CHPL_QTHREAD_ENABLE_OVERSUBSCRIPTION="1",
            CHPL_RT_MASTERIP="127.0.0.1",
            CHPL_RT_WORKERIP="127.0.0.0",
            CHPL_LAUNCHER="",
        ):
            return subprocess.run(["util/test/checkChplInstall"])

    def check_chpl_install(self):
        if self.spec.variants["comm"].value != "none":
            return self.check_chpl_install_gasnet()
        else:
            return subprocess.run(["util/test/checkChplInstall"])

    def test_hello(self):
        """Run the hello world test"""
        with working_dir(self.test_suite.current_test_cache_dir):
            with set_env(CHPL_CHECK_HOME=self.test_suite.current_test_cache_dir):
                with test_part(self, "test_hello", purpose="test hello world"):
                    if self.spec.satisfies("+cuda") or self.spec.satisfies("+rocm"):
                        with set_env(COMP_FLAGS="--no-checks --no-compiler-driver"):
                            res = self.check_chpl_install()
                            assert res and res.returncode == 0
                    else:
                        res = self.check_chpl_install()
                        assert res and res.returncode == 0

    # TODO: This is a pain because the checkChplDoc script doesn't have the same
    # support for CHPL_CHECK_HOME and chpldoc is finicky about CHPL_HOME
    def test_chpldoc(self):
        """Run the chpldoc test"""
        if not self.spec.satisfies("+chpldoc"):
            print("Skipping chpldoc test as chpldoc variant is not set")
            return
        else:
            # TODO: Need to update checkChplDoc to work in the spack testing environment
            pass

    # TODO: In order to run these tests, there's a lot of infrastructure to copy
    # from the Chapel test suite and there are conflicts with CHPL_HOME needing
    # to match the compiler's directory and the test suite's directory
    # def test_package_modules(self):
    #     """Test that the package modules are available"""
    #     # if not self.spec.satisfies("+module_tests"):
    #     #     print("Skipping module tests as module_tests variant is not set")
    #     #     return
    #     tests_to_run = []
    #     with working_dir(self.test_suite.current_test_cache_dir):
    #         with set_env(CHPL_HOME=join_path(self.spec.prefix.share,
    #                      "chapel", self._output_version_short)):
    #             with test_part(self, "test_package_modules", purpose="test package modules"):
    #                 if self.spec.satisfies("+yaml"):
    #                     tests_to_run.append("test/library/packages/Yaml/writeAndParse.chpl")
    #                 if self.spec.satisfies("+zmq"):
    #                     tests_to_run.append("test/library/packages/ZMQ/weather.chpl")
    #                 if self.spec.satisfies("+ssl"):
    #                     tests_to_run.append("test/library/packages/Crypto/")
    #                 # TODO: These tests fail with llvm, unable to find C variable CURLPAUSE_CONT
    #                 if (
    #                     self.spec.satisfies("+curl")
    #                     and self.spec.variants["llvm"].value == "none"
    #                 ):
    #                     with set_env(CHPL_NIGHTLY_TEST_CONFIG_NAME="networking-packages"):
    #                         print("Running package module test for package 'curl'")
    #                         res = subprocess.run(
    #                             ["util/start_test", "test/library/packages/Curl/"]
    #                         )
    #                         assert res.returncode == 0
    #                         print("Running package module test for package 'url'")
    #                         res = subprocess.run(["util/start_test",
    #                                               "test/library/packages/URL/"])
    #                         assert res.returncode == 0
    #                 if self.spec.satisfies("+hdf5"):
    #                     tests_to_run.append("test/library/packages/HDF5/")
    #                 if self.spec.satisfies("+protobuf"):
    #                     tests_to_run.append("test/library/packages/ProtobufProtocolSupport/")
    #                 if len(tests_to_run) > 0:
    #                     with set_env(CHPL_HOME=self.test_suite.current_test_cache_dir):
    #                         compiler = join_path(self.spec.prefix.bin,'chpl')
    #                         print("Running package module tests for packages...")
    #                         print(f" command to run: util/start_test --compiler {compiler}")
    #                         tests_to_run.insert(0, "util/start_test")
    #                         tests_to_run.insert(1, "--compiler")
    #                         tests_to_run.insert(2, compiler)
    #                         res = subprocess.run([t for t in tests_to_run])
    #                         assert res.returncode == 0

    @run_after("install")
    def copy_test_files(self):
        """Copy test files to the install directory"""
        test_files = [
            "test/release/examples",
            "util/start_test",
            "util/test",
            "util/chplenv",
            "util/config",
            "util/printchplenv",
            #   "test/library/packages/Curl",
            #   "test/library/packages/URL/",
            #   "test/library/packages/ProtobufProtocolSupport/",
            #   "test/library/packages/Crypto/",
            #   "test/library/packages/Yaml/",
            #   "test/library/packages/ZMQ/",
            #   "test/library/packages/HDF5/",
            "chplconfig",
            "make",
            "third-party/chpl-venv/",
        ]
        cache_extra_test_sources(self, test_files)

    # @run_after("install")
    # @on_package_attributes(run_tests=True)
    # def self_check(self):
    #     """Run the self-check after installing the package"""
    #     path_put_first("PATH", [self.prefix.bin])
    #     self.test_version()
    #     self.test_hello()
    #     if self.spec.satisfies("+chpldoc"):
    #       make("check-chpldoc")
    #     self.test_package_modules()
