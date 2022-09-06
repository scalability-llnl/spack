# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class RocmSuite(BundlePackage):
    """AMD ROCm Suite.
    """

    maintainers = ["srekolam", "renjithravindrankannath", "haampie", "kwryankrattiger"]
    tags = ["rocm"]

    for _version, version_args in ROCmPackage.rocm_versions.items():
        version(_version, **version_args)
        depends_on("llvm-amdgpu@{0}".format(_version), when="@{0}".format(_version))
        depends_on("hsa-rocr-dev@{0}".format(_version), when="@{0}".format(_version))
        depends_on("hip@{0}".format(_version), when="@{0}".format(_version))
        depends_on("rocm-config@{0}".format(_version), when="@{0}".format(_version))

    # Add compiler minimum versions based on the first release where the
    # processor is included in llvm/lib/Support/TargetParser.cpp
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx900:xnack-")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx906:xnack-")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx908:xnack-")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx90c")
    depends_on("llvm-amdgpu@4.3.0:", when="^rocm-config amdgpu_target=gfx90a")
    depends_on("llvm-amdgpu@4.3.0:", when="^rocm-config amdgpu_target=gfx90a:xnack-")
    depends_on("llvm-amdgpu@4.3.0:", when="^rocm-config amdgpu_target=gfx90a:xnack+")
    depends_on("llvm-amdgpu@5.2.0:", when="^rocm-config amdgpu_target=gfx940")
    depends_on("llvm-amdgpu@4.5.0:", when="^rocm-config amdgpu_target=gfx1013")
    depends_on("llvm-amdgpu@3.8.0:", when="^rocm-config amdgpu_target=gfx1030")
    depends_on("llvm-amdgpu@3.9.0:", when="^rocm-config amdgpu_target=gfx1031")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx1032")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx1033")
    depends_on("llvm-amdgpu@4.3.0:", when="^rocm-config amdgpu_target=gfx1034")
    depends_on("llvm-amdgpu@4.5.0:", when="^rocm-config amdgpu_target=gfx1035")
    depends_on("llvm-amdgpu@5.2.0:", when="^rocm-config amdgpu_target=gfx1036")
    depends_on("llvm-amdgpu@5.3.0:", when="^rocm-config amdgpu_target=gfx1100")
    depends_on("llvm-amdgpu@5.3.0:", when="^rocm-config amdgpu_target=gfx1101")
    depends_on("llvm-amdgpu@5.3.0:", when="^rocm-config amdgpu_target=gfx1102")
    depends_on("llvm-amdgpu@5.3.0:", when="^rocm-config amdgpu_target=gfx1103")
    conflicts("^blt@:0.3.6", when="+rocm")

    # conflicts("cuda-suite")
