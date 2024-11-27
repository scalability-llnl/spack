# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

target_arch_list = (
    "armv7a",
    "armv7a-hf",
    "arm64-v8a",
    "arm64-v8.2-a",
    "x86_32",
    "x86_64",
    "armv8a",
    "armv8.2-a",
    "armv8.6-a",
    "armv8r64",
    "x86",
)


class Armcomputelibrary(SConsPackage):
    """The Arm Compute Library is a collection of low-level machine learning functions optimized
    for Arm® Cortex®-A, Arm® Neoverse® and Arm® Mali™ GPUs architectures.
    The library provides superior performance to other open source alternatives and
    immediate support for new Arm® technologies e.g. SVE2."""

    homepage = "https://arm-software.github.io/ComputeLibrary/latest/"
    url = "https://github.com/ARM-software/ComputeLibrary/archive/refs/tags/v23.02.zip"
    git = "https://github.com/ARM-software/ComputeLibrary.git"

    maintainers("annop-w")

    license("MIT")

    version("23.02", sha256="bed1b24047ce00155e552204bc3983e86f46775414c554a34a7ece931d67ec62")
    version("22.11", sha256="2f70f54d84390625222503ea38650c00c49d4b70bc86a6b9aeeebee9d243865f")
    version("22.08", sha256="5d76d07406b105f0bdf74ef80263236cb03baf0ade882f2bf8446bbc239e0079")
    version("22.05", sha256="8ff308448874c6b72c1ce8d9f28af41d8b47c8e5c43b8ccc069da744e3c0a421")
    version("22.02", sha256="0c1fe30b24e78bf5ca313ee8a33ad95e0d2aaddf64d4518ecec6a95e4bfba6e5")

    depends_on("scons@2.3:")

    phases = ["build"]

    variant("build_type", default="release", values=("release", "debug"), description="Build type")
    variant(
        "threads",
        default="cppthreads",
        values=("cppthreads", "openmp"),
        description="Enable C++11 threads/OpenMP backend. OpenMP backend only "
        "works when building with g++ and not clang++.",
    )
    variant(
        "multi_isa",
        default=False,
        description="Build Multi ISA binary version of library." " Note works only for armv8.2-a.",
    )
    variant(
        "target_arch",
        default="armv7a",
        values=target_arch_list,
        description="Target Architecture. The x86_32 and x86_64 targets can only be"
        " used with neon=0 and opencl=1.",
    )
    variant("sve", default=False, description="Build for SVE.")
    variant("sve2", default=False, description="Build for SVE2.")
    variant("neon", default=True, description="Enable Arm® Neon™ support")
    variant(
        "experimental_dynamic_fusion",
        default=False,
        description="Build the experimental dynamic fusion files.",
    )
    variant(
        "experimental_fixed_format_kernels",
        default=False,
        description="Enable fixed format kernels for GEMM.",
    )
    variant("benchmark_examples", default=False, description="Build benchmark examples programs.")
    variant("validate_examples", default=False, description="Build validate examples programs.")
    variant("validation_tests", default=False, description="Build validation test programs.")
    variant("benchmark_tests", default=False, description="Build benchmark test programs.")

    def build_args(self, spec, prefix):
        args = ["-j{0}".format(make_jobs)]

        if spec.satisfies("build_type=debug"):
            args.append("debug=1")
        elif spec.satisfies("build_type=release"):
            args.append("debug=0")

        if spec.satisfies("threads=openmp"):
            args.append("cppthreads=0")
            args.append("openmp=1")
        elif spec.satisfies("threads=cppthreads"):
            args.append("cppthreads=1")
            args.append("openmp=0")

        arch_value = spec.variants["target_arch"].value
        arch_value += "-sve" if spec.variants["sve"].value else ""
        arch_value += "-sve2" if spec.variants["sve2"].value else ""
        args.append("arch={}".format(arch_value))
        args.append("multi_isa={}".format(int(spec.variants["multi_isa"].value)))
        args.append("neon={}".format(int(spec.variants["neon"].value)))
        args.append(
            "experimental_dynamic_fusion={}".format(
                int(spec.variants["experimental_dynamic_fusion"].value)
            )
        )
        args.append(
            "experimental_fixed_format_kernels={}".format(
                int(spec.variants["experimental_fixed_format_kernels"].value)
            )
        )
        args.append("benchmark_examples={}".format(int(spec.variants["benchmark_examples"].value)))
        args.append("validate_examples={}".format(int(spec.variants["validate_examples"].value)))
        args.append("validation_tests={}".format(int(spec.variants["validation_tests"].value)))
        args.append("benchmark_tests={}".format(int(spec.variants["benchmark_tests"].value)))
        args.append("build=native")
        args.append("install_dir={0}".format(prefix))

        return args

    def setup_build_environment(self, env):
        # Spack compiler wrapper inject -mcpu flag for some targets.
        # This can conflict with -march set in scons script, so override it here.
        env.set("SPACK_TARGET_ARGS", "")

    @property
    def libs(self):
        acl_libs = find_libraries(
            ["libarm_compute", "libarm_compute_core", "libarm_compute_graph"],
            root=self.spec.prefix,
            shared=True,
            recursive=True,
        )
        return acl_libs

    @property
    def headers(self):
        incdir = join_path(self.spec.prefix, "include")
        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    @run_after("build")
    def make_sym_link(self):
        # oneDNN expects header and lib files for ACL in arm_compute/ and build/ directory
        prefix = self.spec.prefix
        symlink(join_path(prefix, "include/arm_compute"), join_path(prefix, "arm_compute"))
        symlink(join_path(prefix, "lib"), join_path(prefix, "build"))

    @run_after("build")
    def copy_additional_header(self):
        # copy some additional header files needed by oneDNN
        cpuinfo_dir = "src/common/cpuinfo"
        mkdirp(join_path(self.spec.prefix, cpuinfo_dir))
        for f in ["CpuInfo.h", "CpuIsaInfo.h", "CpuModel.h"]:
            copy(
                join_path(self.stage.source_path, cpuinfo_dir, f),
                join_path(self.spec.prefix, cpuinfo_dir, f),
            )
