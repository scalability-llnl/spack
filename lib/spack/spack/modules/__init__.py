# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating environment modules, which can
include Tcl non-hierarchical modules, Lua hierarchical modules, and others.
"""

import os
from typing import Dict, Type

import llnl.util.tty as tty

import spack.repo
import spack.spec
import spack.store

from . import common
from .common import BaseModuleFileWriter, disable_modules
from .lmod import LmodModulefileWriter
from .tcl import TclModulefileWriter

__all__ = ["TclModulefileWriter", "LmodModulefileWriter", "disable_modules"]

module_types: Dict[str, Type[BaseModuleFileWriter]] = {
    "tcl": TclModulefileWriter,
    "lmod": LmodModulefileWriter,
}


def get_module(
    module_type, spec: spack.spec.Spec, get_full_path, module_set_name="default", required=True
):
    """Retrieve the module file for a given spec and module type.

    Retrieve the module file for the given spec if it is available. If the
    module is not available, this will raise an exception unless the module
    is excluded or if the spec is installed upstream.

    Args:
        module_type: the type of module we want to retrieve (e.g. lmod)
        spec: refers to the installed package that we want to retrieve a module
            for
        required: if the module is required but excluded, this function will
            print a debug message. If a module is missing but not excluded,
            then an exception is raised (regardless of whether it is required)
        get_full_path: if ``True``, this returns the full path to the module.
            Otherwise, this returns the module name.
        module_set_name: the named module configuration set from modules.yaml
            for which to retrieve the module.

    Returns:
        The module name or path. May return ``None`` if the module is not
        available.
    """
    try:
        upstream = spec.installed_upstream
    except spack.repo.UnknownPackageError:
        upstream, record = spack.store.STORE.db.query_by_spec_hash(spec.dag_hash())
    if upstream:
        module = common.upstream_module_index.upstream_module(spec, module_type)
        if not module:
            return None

        if get_full_path:
            return module.path
        else:
            return module.use_name
    else:
        writer = module_types[module_type](spec, module_set_name)
        if not os.path.isfile(writer.layout.filename):
            fmt_str = "{name}{@version}{/hash:7}"
            if not writer.conf.excluded:
                raise common.ModuleNotFoundError(
                    "The module for package {} should be at {}, but it does not exist".format(
                        spec.format(fmt_str), writer.layout.filename
                    )
                )
            elif required:
                tty.debug(
                    "The module configuration has excluded {}: omitting it".format(
                        spec.format(fmt_str)
                    )
                )
            else:
                return None

        if get_full_path:
            return writer.layout.filename
        else:
            return writer.layout.use_name
