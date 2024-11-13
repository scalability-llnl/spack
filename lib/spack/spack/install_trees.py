# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
For tracking install trees.
"""

import inspect
import os
import pathlib
import warnings

import spack.paths as paths

install_root = None

_old_install_base = os.path.join("prefix", "opt", "spack")

_default_install_base = os.path.join(paths.per_spack_user_root, "installs")

alias = {".root": _old_install_base, ".user": _default_install_base}


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
    elif paths.dir_is_occupied(_default_install_base):
        return _default_install_base
    elif paths.dir_is_occupied(_old_install_base):
        return _old_install_base
    else:
        return _default_install_base


def install_tree_config():
    root = install_tree()
    cfgs = os.path.join(root, "configs")
    return cfgs


def _most_recent_internal_call():
    """If called within an audit for a Python library function, finds
    the most recent spot within Spack's source code that generated
    the call.
    """

    stack = inspect.stack()
    this_file = str(pathlib.Path(__file__).resolve())
    for frame in stack:
        frame_loc = pathlib.Path(frame.filename).resolve()
        if str(frame_loc) != this_file:
            return frame_loc, frame.lineno

    return None, None


_recorded_accesses = set()


def _attempted_modify_internal(msg):
    loc, line = _most_recent_internal_call()
    if loc:
        if (loc, line) not in _recorded_accesses:
            _recorded_accesses.add((loc, line))
            msg += f" at {loc}:{line}"
            warnings.warn(msg)
    else:
        msg += " (no location)"
        warnings.warn(msg)


def _guard_writes(event, args):
    # Note: this doesn't catch files opened in "r" mode and then
    # later upgraded to "w" mode (e.g. our locks). I think to track
    # that properly we would need to (a) patch builtins.open to
    # map all paths to FDs as they are opened (and delete on close)
    # and (b) audit fcntl.fcntl events, using reverse mapping on
    # FD to check associated path
    if event == "open":
        path, mode = args[:2]
        if not mode:
            # Some internal Python libs can call open(..., mode=None)
            return
        if not isinstance(path, str):
            # Skip instances of open() that function like fdopen
            return
        abs_path = os.path.abspath(path)
        intent_to_modify = bool((set(mode) & set("wax")) or "r+" in mode)
        if abs_path.startswith(paths.prefix) and intent_to_modify:
            _attempted_modify_internal(f"Open {path} in mode [{mode}]")
    elif event in ["shutil.copyfile", "os.rename", "shutil.move"]:
        _, dst = args[:2]
        abs_dst = os.path.abspath(dst)
        if abs_dst.startswith(paths.prefix):
            _attempted_modify_internal(f"copy dst {abs_dst}")
    elif event == "os.mkdir":
        path = args[0]
        abs_path = os.path.abspath(path)
        if abs_path.startswith(paths.prefix):
            _attempted_modify_internal(f"mkdir {abs_path}")


def guard_writes_into_spack():
    import sys

    sys.addaudithook(_guard_writes)


def shared_trees():
    return pathlib.Path(paths.system_config_path) / "install-trees"
