# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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
#       `std::__throw_out_of_range_fmt(char const*, ...)@@GLIBCXX_3.4.20`
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
#    /opt/rocm/hsa also has an hsa.h file, but it won"t be found because spack
#    does not like its directory structure.
#

from spack.directives import variant
from spack.package_base import PackageBase


class ROCmPackage(PackageBase):
    """Auxiliary class which contains ROCm variant, and ROCm meta tools
    and is meant to unify and facilitate its usage.

    Maintainers: dtaller, kwryankrattiger
    """

    rocm_versions = {
        "5.4.3":  {"preferred": True},
        "5.4.0":  {"preferred": False},
        "5.3.3":  {"preferred": True},
        "5.3.0":  {"preferred": False},
        "5.2.2":  {"preferred": True},
        "5.2.1":  {"preferred": False},
        "5.2.0":  {"preferred": False},
        "5.1.3":  {"preferred": True},
        "5.1.0":  {"preferred": False},
        # Deprecated Versions
        "5.0.2":  {"deprecated": True},
        "5.0.0":  {"deprecated": True},
        "4.5.2":  {"deprecated": True},
        "4.5.0":  {"deprecated": True},
        "4.3.1":  {"deprecated": True},
        "4.3.0":  {"deprecated": True},
        "4.2.0":  {"deprecated": True},
        "4.1.0":  {"deprecated": True},
        "4.0.0":  {"deprecated": True},
        "3.10.0": {"deprecated": True},
        "3.9.0":  {"deprecated": True},
        "3.8.0":  {"deprecated": True},
        "3.7.0":  {"deprecated": True},
        "3.5.0":  {"deprecated": True}
    }

    amdgpu_targets = (
       # GCN GFX7 Sea Islands
        "gfx700", "gfx701", "gfx702", "gfx703", "gfx704", "gfx705",
        # GCN GFX8 Volcanic Islands
        "gfx801", "gfx802", "gfx803", "gfx805", "gfx810",
        # GCN GFX9 Vega
        "gfx900", "gfx902", "gfx904", "gfx906", "gfx908", "gfx909", "gfx90a",
        "gfx90c",
        # GCN GFX10 RDNA 1
        "gfx1010", "gfx1011", "gfx1012", "gfx1013",
        # GCN GFX10 RDNA 2
        "gfx1030", "gfx1031", "gfx1032", "gfx1033", "gfx1034", "gfx1035", "gfx1036",
        # GCN GFX11 RDNA 3
        "gfx1100", "gfx1101", "gfx1102", "gfx1103",
    )

    amdgpu_target_features = {
        "cumode": (
            "gfx1010", "gfx1011", "gfx1012", "gfx1013",
            "gfx1030", "gfx1031", "gfx1032", "gfx1033", "gfx1034", "gfx1035", "gfx1036",
            "gfx1100", "gfx1101", "gfx1102", "gfx1103"
        ),
        "sramecc": ("gfx906", "gfx908", "gfx90a"),
        "tgsplit": ("gfx90a"),
        "wavefrontsize64": (
            "gfx1010", "gfx1011", "gfx1012", "gfx1013",
            "gfx1030", "gfx1031", "gfx1032", "gfx1033", "gfx1034", "gfx1035", "gfx1036",
            "gfx1100", "gfx1101", "gfx1102", "gfx1103"
        ),
        "xnack": (
            "gfx801", "gfx810",
            "gfx900", "gfx902", "gfx904", "gfx906", "gfx908", "gfx909",
            "gfx90a", "gfx90c",
            "gfx1010", "gfx1011", "gfx1012", "gfx1013"
        )
    }

    variant("rocm", default=False, description="Enable ROCm support")

    depends_on("rocm-suite", when="+rocm")

    # https://github.com/ROCm-Developer-Tools/HIP/blob/master/bin/hipcc
    # It seems that hip-clang does not (yet?) accept this flag, in which case
    # we will still need to set the HCC_AMDGPU_TARGET environment flag in the
    # hip package file. But I will leave this here for future development.
    @staticmethod
    def hip_flags(amdgpu_target):
        archs = ",".join(amdgpu_target)
        return "--amdgpu-target={0}".format(archs)


    # Get the config amdgpu_targets
    @classmethod
    def get_amdgpu_targets(cls, spec):
        targets = []
        if "rocm-config" in spec:
            targets = spec["rocm-config"].variants["amdgpu_target"].value
        return targets


    # Get the config amdgpu_targets without feature strings
    @classmethod
    def get_amdgpu_targets_without_features(cls, spec):
        targets = {}
        if "rocm-config" in spec:
            for target in spec["rocm-config"].variants["amdgpu_target"].value:
                targets.add(target.split(":")[0])
        return [x for x in targets]
