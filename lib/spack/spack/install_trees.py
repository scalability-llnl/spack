# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
For tracking install trees.
"""

import spack.paths as paths

import os

install_root = None

_old_installs_base = os.path.join(paths.internal_opt_path, "spack")

default_install_base = os.path.join(paths.per_spack_user_root, "installs")

alias = {
    ".root": _old_installs_base,
    ".user": default_install_base,
}

def install_tree():
    """
    Selecting install-tree

    - if user specifies --install-root, we use that
    - if $user_root has one, we use that
    - if $old_install_path is occupied, we use that
    - otherwise, we use $user_root
    """
    if install_root:
        # User can e.g. say --install-root=.root to refer to
        # the installation tree inside of the Spack prefix
        return alias.get(install_root, install_root)
    elif paths.dir_is_occupied(default_install_base):
        return default_install_base
    elif paths.dir_is_occupied(_old_installs_base):
        return _old_installs_base
    else:
        return default_install_base


def install_tree_config():
    root = install_tree()
    cfgs = os.path.join(root, "configs")
    return cfgs