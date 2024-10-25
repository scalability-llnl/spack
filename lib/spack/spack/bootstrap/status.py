# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Query the status of bootstrapping on this machine"""
import platform
from typing import List, Optional, Sequence, Tuple, Union

import spack.util.executable

from ._common import _executables_in_store, _python_import, _try_import_from_store
from .config import ensure_bootstrap_configuration
from .core import clingo_root_spec, patchelf_root_spec
from .environment import (
    BootstrapEnvironment,
    black_root_spec,
    flake8_root_spec,
    isort_root_spec,
    mypy_root_spec,
    pytest_root_spec,
)

ExecutablesType = Union[str, Sequence[str]]
RequiredResponseType = Tuple[bool, Optional[str]]
SpecLike = Union["spack.spec.Spec", str]


def _required_system_executable(exes: ExecutablesType, msg: str) -> RequiredResponseType:
    """Search for an executable is the system path only."""
    if isinstance(exes, str):
        exes = (exes,)
    if spack.util.executable.which_string(*exes):
        return True, None
    return False, msg


def _required_executable(
    exes: ExecutablesType, query_spec: SpecLike, msg: str
) -> RequiredResponseType:
    """Search for an executable in the system path or in the bootstrap store."""
    if isinstance(exes, str):
        exes = (exes,)
    if spack.util.executable.which_string(*exes) or _executables_in_store(exes, query_spec):
        return True, None
    return False, msg


def _required_python_module(module: str, query_spec: SpecLike, msg: str) -> RequiredResponseType:
    """Check if a Python module is available in the current interpreter or
    if it can be loaded from the bootstrap store
    """
    if _python_import(module) or _try_import_from_store(module, query_spec):
        return True, None
    return False, msg


def _missing(name: str, purpose: str, system_only: bool = True) -> str:
    """Message to be printed if an executable is not found"""
    msg = '[{2}] MISSING "{0}": {1}'
    if not system_only:
        return msg.format(name, purpose, "@*y{{B}}")
    return msg.format(name, purpose, "@*y{{-}}")


def _core_requirements() -> List[RequiredResponseType]:
    _core_system_exes = {
        "make": _missing("make", "required to build software from sources"),
        "patch": _missing("patch", "required to patch source code before building"),
        "tar": _missing("tar", "required to manage code archives"),
        "gzip": _missing("gzip", "required to compress/decompress code archives"),
        "unzip": _missing("unzip", "required to compress/decompress code archives"),
        "bzip2": _missing("bzip2", "required to compress/decompress code archives"),
        "git": _missing("git", "required to fetch/manage git repositories"),
    }
    if platform.system().lower() == "linux":
        _core_system_exes["xz"] = _missing("xz", "required to compress/decompress code archives")

    # Executables that are not bootstrapped yet
    result = [_required_system_executable(exe, msg) for exe, msg in _core_system_exes.items()]
    # Python modules
    result.append(
        _required_python_module(
            "clingo", clingo_root_spec(), _missing("clingo", "required to concretize specs", False)
        )
    )
    return result


def _buildcache_requirements() -> List[RequiredResponseType]:
    _buildcache_exes = {
        "file": _missing("file", "required to analyze files for buildcaches", system_only=False),
        ("gpg2", "gpg"): _missing("gpg2", "required to sign/verify buildcaches", False),
    }
    if platform.system().lower() == "darwin":
        _buildcache_exes["otool"] = _missing("otool", "required to relocate binaries")

    # Executables that are not bootstrapped yet
    result = [_required_system_executable(exe, msg) for exe, msg in _buildcache_exes.items()]

    if platform.system().lower() == "linux":
        result.append(
            _required_executable(
                "patchelf",
                patchelf_root_spec(),
                _missing("patchelf", "required to relocate binaries", False),
            )
        )

    return result


def _optional_requirements() -> List[RequiredResponseType]:
    _optional_exes = {
        "zstd": _missing("zstd", "required to compress/decompress code archives"),
        "svn": _missing("svn", "required to manage subversion repositories"),
        "hg": _missing("hg", "required to manage mercurial repositories"),
    }
    # Executables that are not bootstrapped yet
    result = [_required_system_executable(exe, msg) for exe, msg in _optional_exes.items()]
    return result


def _development_requirements() -> List[RequiredResponseType]:
    # Ensure we trigger environment modifications if we have an environment
    if BootstrapEnvironment.spack_yaml().exists():
        with BootstrapEnvironment() as env:
            env.load()

    return [
        _required_executable(
            "isort", isort_root_spec(), _missing("isort", "required for style checks", False)
        ),
        _required_executable(
            "mypy", mypy_root_spec(), _missing("mypy", "required for style checks", False)
        ),
        _required_executable(
            "flake8", flake8_root_spec(), _missing("flake8", "required for style checks", False)
        ),
        _required_executable(
            "black", black_root_spec(), _missing("black", "required for code formatting", False)
        ),
        _required_python_module(
            "pytest", pytest_root_spec(), _missing("pytest", "required to run unit-test", False)
        ),
    ]


def status_message(section) -> Tuple[str, bool]:
    """Return a status message to be printed to screen that refers to the
    section passed as argument and a bool which is True if there are missing
    dependencies.

    Args:
        section (str): either 'core' or 'buildcache' or 'optional' or 'develop'
    """
    pass_token, fail_token = "@*g{[PASS]}", "@*r{[FAIL]}"

    # Contain the header of the section and a list of requirements
    spack_sections = {
        "core": ("{0} @*{{Core Functionalities}}", _core_requirements),
        "buildcache": ("{0} @*{{Binary packages}}", _buildcache_requirements),
        "optional": ("{0} @*{{Optional Features}}", _optional_requirements),
        "develop": ("{0} @*{{Development Dependencies}}", _development_requirements),
    }
    msg, required_software = spack_sections[section]

    with ensure_bootstrap_configuration():
        missing_software = False
        for found, err_msg in required_software():
            if not found and err_msg:
                missing_software = True
                msg += "\n  " + err_msg
        msg += "\n"
        msg = msg.format(pass_token if not missing_software else fail_token)
    return msg, missing_software
