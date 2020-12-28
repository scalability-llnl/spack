# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#
# 2. hip and its dependencies are currently NOT picked up by spack
#    automatically, and should therefore be added to packages.yaml by hand:
#
#    in packages.yaml:
#    hip:
#      externals:
#      - spec: hip@3.8.20371-d1886b0b
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
# 3. In part 2, DO NOT list the path to hsa as /opt/rocm/hsa ! You want spack
#    to find hsa in /opt/rocm/include/hsa/hsa.h . The directory of
#    /opt/rocm/hsa also has an hsa.h file, but it won't be found because spack
#    does not like its directory structure.
#

from spack.package_base import PackageBase
from spack.directives import depends_on, variant, conflicts

import spack.variant


class ROCmPackage(PackageBase):
    """Auxiliary class which contains ROCm variant, dependencies and conflicts
    and is meant to unify and facilitate its usage. Closely mimics CudaPackage.

    Maintainers: dtaller
    """

    # https://llvm.org/docs/AMDGPUUsage.html
    # Possible architectures
    amdgpu_targets = (
        'gfx701', 'gfx801', 'gfx802', 'gfx803',
        'gfx900', 'gfx906', 'gfx908', 'gfx1010',
        'gfx1011', 'gfx1012'
    )

    variant('rocm', default=False, description='Enable ROCm support')

    # possible amd gpu targets for rocm builds
    variant('amdgpu_target',
            description='AMD GPU architecture',
            values=spack.variant.any_combination_of(*amdgpu_targets))

    depends_on('llvm-amdgpu', when='+rocm')
    depends_on('hsa-rocr-dev', when='+rocm')
    depends_on('hip', when='+rocm')

    conflicts('^blt@:0.3.6', when='+rocm')

    # need amd gpu type for rocm builds
    conflicts('amdgpu_target=none', when='+rocm')

    # Make sure amdgpu_targets cannot be used without +rocm
    for value in amdgpu_targets:
        conflicts('~rocm', when='amdgpu_target=' + value)

    # https://github.com/ROCm-Developer-Tools/HIP/blob/master/bin/hipcc
    # It seems that hip-clang does not (yet?) accept this flag, in which case
    # we will still need to set the HCC_AMDGPU_TARGET environment flag in the
    # hip package file. But I will leave this here for future development.
    @staticmethod
    def hip_flags(amdgpu_target):
        archs = ",".join(amdgpu_target)
        return '--amdgpu-target={0}'.format(archs)

    # HIP version vs Architecture

    # TODO: add a bunch of lines like:
    # depends_on('hip@:6.0', when='amdgpu_target=gfx701')
    # to indicate minimum version for each architecture.

    # Compiler conflicts

    # TODO: add conflicts statements along the lines of
    # arch_platform = ' target=x86_64: platform=linux'
    # conflicts('%gcc@5:', when='+cuda ^cuda@:7.5' + arch_platform)
    # conflicts('platform=darwin', when='+cuda ^cuda@11.0.2:')
    # for hip-related limitations.
