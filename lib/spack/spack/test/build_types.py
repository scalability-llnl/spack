# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_types
from spack.util.naming import class_to_mod


def test_class_to_mod():
    """
    Ensure that every module in build_types has a key via class_to_mod.
    """
    build_type = class_to_mod("DebugMax")
    assert build_type in spack.build_types.build_types


def test_build_type_flags():
    """
    Every build type is required to have a known set of flag attributes.
    """
    for build_type in spack.build_types.build_types.values():
        assert hasattr(build_type, "compiler_attrs")
        assert hasattr(build_type, "cuda_attrs")
