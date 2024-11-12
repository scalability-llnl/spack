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


def shared_trees():
    root_dir = pathlib.Path(paths.system_config_path) / "install-trees"
