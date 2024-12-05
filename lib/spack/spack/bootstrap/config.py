# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Manage configuration swapping for bootstrapping purposes"""

import contextlib
import os.path
import sys
from typing import Any, Dict, Generator, MutableSequence, Sequence

from llnl.util import tty

import spack.compilers
import spack.config
import spack.environment
import spack.modules
import spack.paths
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.util.path

#: Reference counter for the bootstrapping configuration context manager
_REF_COUNT = 0


def is_bootstrapping() -> bool:
    """Return True if we are in a bootstrapping context, False otherwise."""
    return _REF_COUNT > 0


def spec_for_current_python() -> str:
    """For bootstrapping purposes we are just interested in the Python
    minor version (all patches are ABI compatible with the same minor).

    See:
      https://www.python.org/dev/peps/pep-0513/
      https://stackoverflow.com/a/35801395/771663
    """
    version_str = ".".join(str(x) for x in sys.version_info[:2])
    return f"python@{version_str}"


def root_path() -> str:
    """Root of all the bootstrap related folders"""
    return spack.util.path.canonicalize_path(
        spack.config.get("bootstrap:root", spack.paths.default_user_bootstrap_path)
    )


def store_path() -> str:
    """Path to the store used for bootstrapped software"""
    enabled = spack.config.get("bootstrap:enable", True)
    if not enabled:
        msg = 'bootstrapping is currently disabled. Use "spack bootstrap enable" to enable it'
        raise RuntimeError(msg)

    return _store_path()


@contextlib.contextmanager
def spack_python_interpreter() -> Generator:
    """Override the current configuration to set the interpreter under
    which Spack is currently running as the only Python external spec
    available.
    """
    python_prefix = sys.exec_prefix
    external_python = spec_for_current_python()

    entry = {
        "buildable": False,
        "externals": [{"prefix": python_prefix, "spec": str(external_python)}],
    }

    with spack.config.override("packages:python::", entry):
        yield


def _store_path() -> str:
    bootstrap_root_path = root_path()
    return spack.util.path.canonicalize_path(os.path.join(bootstrap_root_path, "store"))


def _config_path() -> str:
    bootstrap_root_path = root_path()
    return spack.util.path.canonicalize_path(os.path.join(bootstrap_root_path, "config"))


@contextlib.contextmanager
def ensure_bootstrap_configuration() -> Generator:
    """Swap the current configuration for the one used to bootstrap Spack.

    The context manager is reference counted to ensure we don't swap multiple
    times if there's nested use of it in the stack. One compelling use case
    is bootstrapping patchelf during the bootstrap of clingo.
    """
    global _REF_COUNT  # pylint: disable=global-statement
    already_swapped = bool(_REF_COUNT)
    _REF_COUNT += 1
    try:
        if already_swapped:
            yield
        else:
            with _ensure_bootstrap_configuration():
                yield
    finally:
        _REF_COUNT -= 1


def _read_and_sanitize_configuration() -> Dict[str, Any]:
    """Read the user configuration that needs to be reused for bootstrapping
    and remove the entries that should not be copied over.
    """
    # Read the "config" section but pop the install tree (the entry will not be
    # considered due to the use_store context manager, so it will be confusing
    # to have it in the configuration).
    config_yaml = spack.config.get("config")
    config_yaml.pop("install_tree", None)
    user_configuration = {"bootstrap": spack.config.get("bootstrap"), "config": config_yaml}
    return user_configuration


def _bootstrap_config_scopes() -> Sequence["spack.config.ConfigScope"]:
    tty.debug("[BOOTSTRAP CONFIG SCOPE] name=_builtin")
    config_scopes: MutableSequence["spack.config.ConfigScope"] = [
        spack.config.InternalConfigScope("_builtin", spack.config.CONFIG_DEFAULTS)
    ]
    configuration_paths = (spack.config.CONFIGURATION_DEFAULTS_PATH, ("bootstrap", _config_path()))
    for name, path in configuration_paths:
        platform = spack.platforms.host().name
        platform_scope = spack.config.DirectoryConfigScope(
            f"{name}/{platform}", os.path.join(path, platform)
        )
        generic_scope = spack.config.DirectoryConfigScope(name, path)
        config_scopes.extend([generic_scope, platform_scope])
        msg = "[BOOTSTRAP CONFIG SCOPE] name={0}, path={1}"
        tty.debug(msg.format(generic_scope.name, generic_scope.path))
        tty.debug(msg.format(platform_scope.name, platform_scope.path))
    return config_scopes


def _add_compilers_if_missing() -> None:
    arch = spack.spec.ArchSpec.frontend_arch()
    if not spack.compilers.compilers_for_arch(arch):
        spack.compilers.find_compilers()


@contextlib.contextmanager
def _ensure_bootstrap_configuration() -> Generator:
    spack.store.ensure_singleton_created()
    bootstrap_store_path = store_path()
    user_configuration = _read_and_sanitize_configuration()
    with spack.environment.no_active_environment():
        with spack.platforms.use_platform(
            spack.platforms.real_host()
        ), spack.repo.use_repositories(spack.paths.packages_path):
            # Default configuration scopes excluding command line
            # and builtin but accounting for platform specific scopes
            config_scopes = _bootstrap_config_scopes()
            with spack.config.use_configuration(*config_scopes), spack.store.use_store(
                bootstrap_store_path, extra_data={"padded_length": 0}
            ):
                # We may need to compile code from sources, so ensure we
                # have compilers for the current platform
                _add_compilers_if_missing()
                spack.config.set("bootstrap", user_configuration["bootstrap"])
                spack.config.set("config", user_configuration["config"])
                with spack.modules.disable_modules():
                    with spack_python_interpreter():
                        yield
