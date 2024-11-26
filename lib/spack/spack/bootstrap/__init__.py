# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Function and classes needed to bootstrap Spack itself."""

from .config import ensure_bootstrap_configuration, is_bootstrapping, store_path
from .core import (
    all_core_root_specs,
    ensure_clingo_importable_or_raise,
    ensure_core_dependencies,
    ensure_file_in_path_or_raise,
    ensure_gpg_in_path_or_raise,
    ensure_patchelf_in_path_or_raise,
)
from .environment import BootstrapEnvironment, ensure_environment_dependencies
from .status import status_message

__all__ = [
    "is_bootstrapping",
    "ensure_bootstrap_configuration",
    "ensure_core_dependencies",
    "ensure_file_in_path_or_raise",
    "ensure_gpg_in_path_or_raise",
    "ensure_clingo_importable_or_raise",
    "ensure_patchelf_in_path_or_raise",
    "all_core_root_specs",
    "ensure_environment_dependencies",
    "BootstrapEnvironment",
    "status_message",
    "store_path",
]
