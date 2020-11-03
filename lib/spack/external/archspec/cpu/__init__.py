# Copyright 2019-2020 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""The "cpu" package permits to query and compare different
CPU microarchitectures.
"""
from .microarchitecture import Microarchitecture, UnsupportedMicroarchitecture
from .microarchitecture import TARGETS, generic_microarchitecture
from .microarchitecture import version_components
from .detect import host

__all__ = [
    "Microarchitecture",
    "UnsupportedMicroarchitecture",
    "TARGETS",
    "generic_microarchitecture",
    "host",
    "version_components",
]
