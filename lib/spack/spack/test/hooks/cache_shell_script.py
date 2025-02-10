# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

import spack.hooks.cache_shell_script as shell_script
from spack.main import SpackCommand
from spack.spec import Spec

install = SpackCommand("install")


@pytest.mark.parametrize(
    "shell,set_command",
    (
        [
            ("sh", "export %s=%s"),
            ("csh", "setenv %s %s"),
            ("fish", "set %s %s"),
            ("bat", 'set "%s=%s"'),
            ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else [("sh", "export %s=%s"), ("csh", "setenv %s %s"), ("fish", "set %s %s")]
    ),
)
def test_paths_to_shell_cached(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test does a thing"""

    spec = Spec("mpileaks")
    spec.concretize()

    install(spec.name)

    for pkg in spec.traverse():
        path_to_load_shell = os.path.join(pkg.prefix, ".spack", f"load.{shell}")
        script_path_to_load_shell = shell_script.path_to_load_shell_script(pkg, shell)

        assert path_to_load_shell == script_path_to_load_shell

        path_to_unload_shell = os.path.join(pkg.prefix, ".spack", f"unload.{shell}")
        script_path_to_unload_shell = shell_script.path_to_unload_shell_script(pkg, shell)

        assert path_to_unload_shell == script_path_to_unload_shell


# import util environment's _SHELL_SET_STRINGS??
@pytest.mark.parametrize(
    "shell,set_command",
    (
        [
            ("sh", "export %s=%s"),
            ("csh", "setenv %s %s"),
            ("fish", "set %s %s"),
            ("bat", 'set "%s=%s"'),
            ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else [("sh", "export %s=%s"), ("csh", "setenv %s %s"), ("fish", "set %s %s")]
    ),
)
def test_install_shell_cached(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test does a thing"""

    spec = Spec("mpileaks")
    spec.concretize()

    install(spec.name)

    for pkg in spec.traverse():
        path_to_load_shell = shell_script.path_to_load_shell_script(pkg, shell)
        path_to_unload_shell = shell_script.path_to_unload_shell_script(pkg, shell)

        assert os.path.isfile(path_to_load_shell)
        assert os.path.isfile(path_to_unload_shell)


@pytest.mark.parametrize(
    "shell,set_command",
    (
        [
            ("sh", "export %s=%s"),
            ("csh", "setenv %s %s"),
            ("fish", "set %s %s"),
            ("bat", 'set "%s=%s"'),
            ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else [("sh", "export %s=%s"), ("csh", "setenv %s %s"), ("fish", "set %s %s")]
    ),
)
def test_install_with_individual_shell_scripts(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
):  # get better name
    """Test does a thing"""

    callpath_spec = Spec("callpath")
    dyninst_spec = Spec("dyninst")
    mpich_spec = Spec("mpich")

    callpath_spec.concretize()
    dyninst_spec.concretize()
    mpich_spec.concretize()

    install(callpath_spec.name)

    path_to_dyninst = shell_script.path_to_load_shell_script(dyninst_spec, shell)
    path_to_mpich = shell_script.path_to_load_shell_script(mpich_spec, shell)

    with open(path_to_dyninst, "r") as f:
        dyninst_shell = f.read()

    with open(path_to_mpich, "r") as f:
        mpich_shell = f.read()

    assert mpich_spec.name not in dyninst_shell
    assert dyninst_spec.name not in mpich_shell


@pytest.mark.parametrize(
    "shell,set_command",
    (
        [
            ("sh", "export %s=%s"),
            ("csh", "setenv %s %s"),
            ("fish", "set %s %s"),
            ("bat", 'set "%s=%s"'),
            ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else [("sh", "export %s=%s"), ("csh", "setenv %s %s"), ("fish", "set %s %s")]
    ),
)
def test_install_multiple_specs(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test does a thing"""

    dyninst_spec = Spec("dyninst")
    hypre_spec = Spec("hypre")

    dyninst_spec.concretize()
    hypre_spec.concretize()

    # Install multiple specs
    install(dyninst_spec.name, hypre_spec.name)

    # no overlap in shell sc
    path_to_dyninst = shell_script.path_to_load_shell_script(dyninst_spec, shell)
    path_to_hypre = shell_script.path_to_load_shell_script(hypre_spec, shell)

    with open(path_to_dyninst, "r") as f:
        dyninst_shell = f.read()

    with open(path_to_hypre, "r") as f:
        hypre_shell = f.read()

    assert hypre_spec.name not in dyninst_shell
    assert dyninst_spec.name not in hypre_shell
