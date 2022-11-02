# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

import itertools

from spack.package import *

def target_strip_feature(target):
    return target.split(":")[0]

class RocmConfig(BundlePackage):
    """Target and Version configurations for ROCm Stacks"""

    # ROCm stack versions available in Spack
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

    maintainers = ["kwryankrattiger"]
    tags = ["rocm"]

    # Setup ROCm versions
    for _version in rocm_versions.keys():
        version(_version)

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=spack.variant.any_combination_of(*ROCmPackage.amdgpu_targets_with_features(features=("xnact", "sramecc")))
    )

    variant(
        "multi-target",
        default=True,
        description="Allow multiple AMD GPU architectures")

    # Setup conflicts for ~multi-target
    for _target, _other_target in itertools.permutations(ROCmPackage.amdgpu_targets, 2):
        conflicts(
            "amdgpu_target={0}".format(_target),
            when="~multi-target amdgpu_target={0}".format(_other_target),
            msg="Only one AMD GPU target may be enabled."
        )

    # Allow targets to include list of features
    for _target in amdgpu_targets:
        for _feature, _targets in ROCmPackage.amdgpu_target_features.items():
            if not _feature in ["xnact", "sramecc"]:
                continue

            for _feature_target in _targets:
                if not _target == _feature_target:
                    conflicts(
                        "amdgpu_target={0}".format(_target),
                        when="~multi-target amdgpu_target={0}:+{1}".format(_feature_target, _feature),
                        msg="Only one AMD GPU target may be enabled."
                    )
                    conflicts(
                        "amdgpu_target={0}".format(_target),
                        when="~multi-target amdgpu_target={0}:-{1}".format(_feature_target, _feature),
                        msg="Only one AMD GPU target may be enabled."
                    )

    conflicts("amdgpu_target=none")
