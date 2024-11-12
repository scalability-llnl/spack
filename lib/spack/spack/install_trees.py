# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
For tracking install trees.
"""

import spack.paths as paths
import spack.util.hash as hash

import pathlib


def use_new_root():
    internal_opt_dir = pathlib.Path(paths.internal_opt_path)
    # If the spack-internal opt/ dir is nonempty, we are using the old
    # root
    return not (internal_opt_dir.is_dir() and any(internal_opt_dir.iterdir()))



def user_root():
    """Default install tree and config scope.

    Applies when $spack/opt is not an install tree.

    ~/<spack-prefix-hash>/
    """
    spack_prefix = paths.prefix
    return pathlib.Path(paths.user_config_path, hash.b32_hash(spack_prefix)[:7])


def shared_trees():
    root_dir = pathlib.Path(paths.system_config_path) / "install-trees"
