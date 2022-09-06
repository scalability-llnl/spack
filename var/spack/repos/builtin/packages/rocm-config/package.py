# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install rocm-config
#
# You can edit this file again by typing:
#
#     spack edit rocm-config
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import itertools

from spack.package import *


class RocmConfig(BundlePackage):
    """Target and Version configurations for ROCm Stacks"""

    maintainers = ["kwryankrattiger"]
    tags = ["rocm"]

    # Setup ROCm versions
    for _version in ROCmPackage.rocm_versions.keys():
        version(_version)

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=spack.variant.any_combination_of(*ROCmPackage.amdgpu_targets_with_features())
    )
    variant("multi-target", default=True,
        description="Allow multiple AMD GPU architectures")

    # Setup conflicts for ~multi-target
    for _target, _other_target in itertools.permutations(ROCmPackage.amdgpu_targets, 2):
        conflicts(
            "amdgpu_target={0}".format(_target),
            when="~multi-target amdgpu_target={0}".format(_other_target),
            msg="Only one AMD GPU target may be enabled."
        )
    for _target in ROCmPackage.amdgpu_targets:
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
