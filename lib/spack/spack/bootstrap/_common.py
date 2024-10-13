# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Common basic functions used through the spack.bootstrap package"""
import fnmatch
import importlib
import os.path
import re
import sys
import sysconfig
import warnings
from typing import Dict, Optional, Sequence, Union

import archspec.cpu

import llnl.util.filesystem as fs
from llnl.util import tty

import spack.platforms
import spack.store
import spack.util.environment
import spack.util.executable

from .config import spec_for_current_python

QueryInfo = Dict[str, "spack.spec.Spec"]


def _python_import(module: str) -> bool:
    try:
        importlib.import_module(module)
    except ImportError:
        return False
    return True


def _try_import_from_store(
    module: str, query_spec: Union[str, "spack.spec.Spec"], query_info: Optional[QueryInfo] = None
) -> bool:
    """Return True if the module can be imported from an already
    installed spec, False otherwise.

    Args:
        module: Python module to be imported
        query_spec: spec that may provide the module
        query_info (dict or None): if a dict is passed it is populated with the
            command found and the concrete spec providing it
    """
    # If it is a string assume it's one of the root specs by this module
    if isinstance(query_spec, str):
        # We have to run as part of this python interpreter
        query_spec += " ^" + spec_for_current_python()

    installed_specs = spack.store.STORE.db.query(query_spec, installed=True)

    for candidate_spec in installed_specs:
        # previously bootstrapped specs may not have a python-venv dependency.
        if candidate_spec.dependencies("python-venv"):
            python, *_ = candidate_spec.dependencies("python-venv")
        else:
            python, *_ = candidate_spec.dependencies("python")
        module_paths = [
            os.path.join(candidate_spec.prefix, python.package.purelib),
            os.path.join(candidate_spec.prefix, python.package.platlib),
        ]
        path_before = list(sys.path)

        # NOTE: try module_paths first and last, last allows an existing version in path
        # to be picked up and used, possibly depending on something in the store, first
        # allows the bootstrap version to work when an incompatible version is in
        # sys.path
        orders = [module_paths + sys.path, sys.path + module_paths]
        for path in orders:
            sys.path = path
            try:
                _fix_ext_suffix(candidate_spec)
                if _python_import(module):
                    msg = (
                        f"[BOOTSTRAP MODULE {module}] The installed spec "
                        f'"{query_spec}/{candidate_spec.dag_hash()}" '
                        f'provides the "{module}" Python module'
                    )
                    tty.debug(msg)
                    if query_info is not None:
                        query_info["spec"] = candidate_spec
                    return True
            except Exception as exc:  # pylint: disable=broad-except
                msg = (
                    "unexpected error while trying to import module "
                    f'"{module}" from spec "{candidate_spec}" [error="{str(exc)}"]'
                )
                warnings.warn(msg)
            else:
                msg = "Spec {0} did not provide module {1}"
                warnings.warn(msg.format(candidate_spec, module))

        sys.path = path_before

    return False


def _fix_ext_suffix(candidate_spec: "spack.spec.Spec"):
    """Fix the external suffixes of Python extensions on the fly for
    platforms that may need it

    Args:
        candidate_spec (Spec): installed spec with a Python module
            to be checked.
    """
    # Here we map target families to the patterns expected
    # by pristine CPython. Only architectures with known issues
    # are included. Known issues:
    #
    # [RHEL + ppc64le]: https://github.com/spack/spack/issues/25734
    #
    _suffix_to_be_checked = {
        "ppc64le": {
            "glob": "*.cpython-*-powerpc64le-linux-gnu.so",
            "re": r".cpython-[\w]*-powerpc64le-linux-gnu.so",
            "fmt": r"{module}.cpython-{major}{minor}m-powerpc64le-linux-gnu.so",
        }
    }

    # If the current architecture is not problematic return
    generic_target = archspec.cpu.host().family
    if str(generic_target) not in _suffix_to_be_checked:
        return

    # If there's no EXT_SUFFIX (Python < 3.5) or the suffix matches
    # the expectations, return since the package is surely good
    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")
    if ext_suffix is None:
        return

    expected = _suffix_to_be_checked[str(generic_target)]
    if fnmatch.fnmatch(ext_suffix, expected["glob"]):
        return

    # If we are here it means the current interpreter expects different names
    # than pristine CPython. So:
    # 1. Find what we have installed
    # 2. Create symbolic links for the other names, it they're not there already

    # Check if standard names are installed and if we have to create
    # link for this interpreter
    standard_extensions = fs.find(candidate_spec.prefix, expected["glob"])
    link_names = [re.sub(expected["re"], ext_suffix, s) for s in standard_extensions]
    for file_name, link_name in zip(standard_extensions, link_names):
        if os.path.exists(link_name):
            continue
        os.symlink(file_name, link_name)

    # Check if this interpreter installed something and we have to create
    # links for a standard CPython interpreter
    non_standard_extensions = fs.find(candidate_spec.prefix, "*" + ext_suffix)
    for abs_path in non_standard_extensions:
        directory, filename = os.path.split(abs_path)
        module = filename.split(".")[0]
        link_name = os.path.join(
            directory,
            expected["fmt"].format(
                module=module, major=sys.version_info[0], minor=sys.version_info[1]
            ),
        )
        if os.path.exists(link_name):
            continue
        os.symlink(abs_path, link_name)


def _executables_in_store(
    executables: Sequence[str],
    query_spec: Union["spack.spec.Spec", str],
    query_info: Optional[QueryInfo] = None,
) -> bool:
    """Return True if at least one of the executables can be retrieved from
    a spec in store, False otherwise.

    The different executables must provide the same functionality and are
    "alternate" to each other, i.e. the function will exit True on the first
    executable found.

    Args:
        executables: list of executables to be searched
        query_spec: spec that may provide the executable
        query_info (dict or None): if a dict is passed it is populated with the
            command found and the concrete spec providing it
    """
    executables_str = ", ".join(executables)
    msg = "[BOOTSTRAP EXECUTABLES {0}] Try installed specs with query '{1}'"
    tty.debug(msg.format(executables_str, query_spec))
    installed_specs = spack.store.STORE.db.query(query_spec, installed=True)
    if installed_specs:
        for concrete_spec in installed_specs:
            bin_dir = concrete_spec.prefix.bin
            # IF we have a "bin" directory and it contains
            # the executables we are looking for
            if (
                os.path.exists(bin_dir)
                and os.path.isdir(bin_dir)
                and spack.util.executable.which_string(*executables, path=bin_dir)
            ):
                spack.util.environment.path_put_first("PATH", [bin_dir])
                if query_info is not None:
                    query_info["command"] = spack.util.executable.which(*executables, path=bin_dir)
                    query_info["spec"] = concrete_spec
                return True
    return False


def _root_spec(spec_str: str) -> str:
    """Add a proper compiler and target to a spec used during bootstrapping.

    Args:
        spec_str: spec to be bootstrapped. Must be without compiler and target.
    """
    # Add a compiler and platform requirement to the root spec.
    platform = str(spack.platforms.host())

    if platform == "darwin":
        spec_str += " %apple-clang"
    elif platform == "windows":
        spec_str += " %msvc"
    elif platform == "linux":
        spec_str += " %gcc"
    elif platform == "freebsd":
        spec_str += " %clang"
    spec_str += f" platform={platform}"
    target = archspec.cpu.host().family
    spec_str += f" target={target}"

    tty.debug(f"[BOOTSTRAP ROOT SPEC] {spec_str}")
    return spec_str
