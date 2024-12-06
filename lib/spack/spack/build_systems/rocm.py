# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Troubleshooting advice for +rocm builds:
#
# 1. When building with clang, go your compilers.yaml,
#    add an entry for the amd version of clang, as below.
#    This will ensure that your entire package is compiled/linked
#    with the same compiler version. If you use a different version of
#    clang which is linked against a different version of the gcc library,
#    you will get errors along the lines of:
#    undefined reference to
#       `std::__throw_out_of_range_fmt(char const*, ...)@@GLIBCXX_3.4.20'
#    which is indicative of a mismatch in standard library versions.
#
#    in compilers.yaml
#    - compiler:
#        spec: clang@amd
#        paths:
#          cc: /opt/rocm/llvm/bin/clang
#          cxx: /opt/rocm/llvm/bin/clang++
#          f77:
#          fc:
#        flags: {}
#        operating_system: rhel7
#        target: x86_64
#        modules: []
#        environment: {}
#        extra_rpaths: []
#
#    It is advisable to replace /rocm/ in the paths above with /rocm-version/
#    and introduce spec version numbers to ensure reproducible results.
#
# 2. hip and its dependencies are currently NOT picked up by spack
#    automatically, and should therefore be added to packages.yaml by hand:
#
#    in packages.yaml:
#    hip:
#      externals:
#      - spec: hip
#        prefix: /opt/rocm/hip
#        extra_attributes:
#          compilers:
#            c: /opt/rocm/llvm/bin/clang++
#            c++: /opt/rocm/llvm/bin/clang++
#            hip: /opt/rocm/hip/bin/hipcc
#      buildable: false
#    hsa-rocr-dev:
#      externals:
#      - spec: hsa-rocr-dev
#        prefix: /opt/rocm
#        extra_attributes:
#          compilers:
#            c: /opt/rocm/llvm/bin/clang++
#            cxx: /opt/rocm/llvm/bin/clang++
#      buildable: false
#    llvm-amdgpu:
#      externals:
#      - spec: llvm-amdgpu
#        prefix: /opt/rocm/llvm
#        extra_attributes:
#          compilers:
#            c: /opt/rocm/llvm/bin/clang++
#            cxx: /opt/rocm/llvm/bin/clang++
#      buildable: false
#
#    It is advisable to replace /rocm/ in the paths above with /rocm-version/
#    and introduce spec version numbers to ensure reproducible results.
#
# 3. In part 2, DO NOT list the path to hsa as /opt/rocm/hsa ! You want spack
#    to find hsa in /opt/rocm/include/hsa/hsa.h . The directory of
#    /opt/rocm/hsa also has an hsa.h file, but it won't be found because spack
#    does not like its directory structure.
#

import os

import spack.variant
from spack.directives import conflicts, depends_on, variant
from spack.package_base import PackageBase
from spack.util.environment import EnvironmentModifications


class ROCmPackage(PackageBase):
    """Auxiliary class which contains ROCm variant, dependencies and conflicts
    and is meant to unify and facilitate its usage. Closely mimics CudaPackage.

    Maintainers: dtaller
    """

    # https://llvm.org/docs/AMDGPUUsage.html
    # Possible architectures
    amdgpu_targets = (
        "gfx701",
        "gfx801",
        "gfx802",
        "gfx803",
        "gfx900",
        "gfx900:xnack-",
        "gfx902",
        "gfx904",
        "gfx906",
        "gfx906:xnack-",
        "gfx908",
        "gfx908:xnack-",
        "gfx909",
        "gfx90a",
        "gfx90a:xnack-",
        "gfx90a:xnack+",
        "gfx90c",
        "gfx940",
        "gfx941",
        "gfx942",
        "gfx1010",
        "gfx1011",
        "gfx1012",
        "gfx1013",
        "gfx1030",
        "gfx1031",
        "gfx1032",
        "gfx1033",
        "gfx1034",
        "gfx1035",
        "gfx1036",
        "gfx1100",
        "gfx1101",
        "gfx1102",
        "gfx1103",
    )

    variant("rocm", default=False, description="Enable ROCm support")

    # possible amd gpu targets for rocm builds
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=spack.variant.any_combination_of(*amdgpu_targets),
        sticky=True,
        when="+rocm",
    )

    depends_on("llvm-amdgpu", when="+rocm")
    depends_on("hsa-rocr-dev", when="+rocm")
    depends_on("hip +rocm", when="+rocm")

    # need amd gpu type for rocm builds
    conflicts("amdgpu_target=none", when="+rocm")

    # https://github.com/ROCm-Developer-Tools/HIP/blob/master/bin/hipcc
    # It seems that hip-clang does not (yet?) accept this flag, in which case
    # we will still need to set the HCC_AMDGPU_TARGET environment flag in the
    # hip package file. But I will leave this here for future development.
    @staticmethod
    def hip_flags(amdgpu_target):
        archs = ",".join(amdgpu_target)
        return "--amdgpu-target={0}".format(archs)

    def asan_on(self, env: EnvironmentModifications):
        llvm_path = self.spec["llvm-amdgpu"].prefix
        env.set("CC", llvm_path + "/bin/clang")
        env.set("CXX", llvm_path + "/bin/clang++")
        env.set("ASAN_OPTIONS", "detect_leaks=0")

        for root, _, files in os.walk(llvm_path):
            if "libclang_rt.asan-x86_64.so" in files:
                asan_lib_path = root
        env.prepend_path("LD_LIBRARY_PATH", asan_lib_path)
        if "rhel" in self.spec.os or "sles" in self.spec.os:
            SET_DWARF_VERSION_4 = "-gdwarf-5"
        else:
            SET_DWARF_VERSION_4 = ""

        env.set("CFLAGS", f"-fsanitize=address -shared-libasan -g {SET_DWARF_VERSION_4}")
        env.set("CXXFLAGS", f"-fsanitize=address -shared-libasan -g {SET_DWARF_VERSION_4}")
        env.set("LDFLAGS", "-Wl,--enable-new-dtags -fuse-ld=lld  -fsanitize=address -g -Wl,")

    # HIP version vs Architecture

    # TODO: add a bunch of lines like:
    # depends_on('hip@:6.0', when='amdgpu_target=gfx701')
    # to indicate minimum version for each architecture.

    # Add compiler minimum versions based on the first release where the
    # processor is included in llvm/lib/Support/TargetParser.cpp
    depends_on("llvm-amdgpu@5.2.0:", when="amdgpu_target=gfx940")
    depends_on("llvm-amdgpu@5.7.0:", when="amdgpu_target=gfx941")
    depends_on("llvm-amdgpu@5.7.0:", when="amdgpu_target=gfx942")
    depends_on("llvm-amdgpu@5.2.0:", when="amdgpu_target=gfx1036")
    depends_on("llvm-amdgpu@5.3.0:", when="amdgpu_target=gfx1100")
    depends_on("llvm-amdgpu@5.3.0:", when="amdgpu_target=gfx1101")
    depends_on("llvm-amdgpu@5.3.0:", when="amdgpu_target=gfx1102")
    depends_on("llvm-amdgpu@5.3.0:", when="amdgpu_target=gfx1103")

    # Compiler conflicts

    # TODO: add conflicts statements along the lines of
    # arch_platform = ' target=x86_64: platform=linux'
    # conflicts('%gcc@5:', when='+cuda ^cuda@:7.5' + arch_platform)
    # conflicts('platform=darwin', when='+cuda ^cuda@11.0.2:')
    # for hip-related limitations.
