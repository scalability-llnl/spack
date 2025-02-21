# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import sys

import pytest

import spack.hooks.cache_shell_script as shell_script
import spack.spec
import spack.user_environment as uenv
from spack.main import SpackCommand

load = SpackCommand("load")
unload = SpackCommand("unload")
install = SpackCommand("install")
location = SpackCommand("location")


def test_load_recursive(install_mockery, mock_fetch, mock_archive, mock_packages, working_env):
    def test_load_shell(shell, set_command):
        """Test that `spack load` applies prefix inspections of its required runtime deps in
        topo-order"""
        install("mpileaks")
        mpileaks_spec = spack.spec.Spec("mpileaks").concretized()

        # Ensure our reference variable is clean.
        os.environ["CMAKE_PREFIX_PATH"] = "/hello" + os.pathsep + "/world"

        shell_out = load(shell, "mpileaks")

        load_script_file = shell_script.path_to_load_shell_script(mpileaks_spec, shell[2:])

        with open(load_script_file, "r") as f:
            shell_out = f.read()

        def extract_value(output, variable):
            value = []
            for line in output.splitlines():
                info = line.split(" ")
                if info[1] == variable:
                    value.append(info[2])
            return value

        # Map a prefix found in CMAKE_PREFIX_PATH back to a package name in mpileaks' DAG.
        prefix_to_pkg = lambda prefix: next(
            s.name for s in mpileaks_spec.traverse() if s.prefix == prefix
        )

        paths_shell = extract_value(shell_out, "CMAKE_PREFIX_PATH")

        # All but the last two paths are added by spack load; lookup what packages they're from.
        pkgs = [prefix_to_pkg(p) for p in paths_shell]

        # Do we have all the runtime packages?
        assert set(pkgs) == set(
            s.name for s in mpileaks_spec.traverse(deptype=("link", "run"), root=True)
        )

        # Finally, do we list them in topo order?
        for i, pkg in enumerate(pkgs):
            set(s.name for s in mpileaks_spec[pkg].traverse(direction="parents")) in set(pkgs[:i])

        # Lastly, do we keep track that mpileaks was loaded?
        assert (
            extract_value(shell_out, uenv.spack_loaded_hashes_var)[0] == mpileaks_spec.dag_hash()
        )
        return paths_shell

    if sys.platform == "win32":
        shell, set_command = ("--bat", r'set "%s=(.*)"')
        test_load_shell(shell, set_command)
    else:
        # TODO: It might not always be _spack_env_prepend. Update to accommodate
        params = [("--sh", r"_spack_env_prepend %s([^:]*)"), ("--csh", r"setenv %s ([^;]*)")]
        shell, set_command = params[0]
        paths_sh = test_load_shell(shell, set_command)
        shell, set_command = params[1]
        paths_csh = test_load_shell(shell, set_command)
        assert paths_sh == paths_csh


# TODO: Reinstate --csh when it's shell script is written
@pytest.mark.parametrize(
    "shell,set_command",
    (
        [("--bat", 'set "%s=%s"')]
        if sys.platform == "win32"
        else [("--sh", "spack_env_set %s %s")]  #, ("--csh", "setenv %s %s")]
    ),
)
def test_load_includes_run_env(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Tests that environment changes from the package's
    `setup_run_environment` method are added to the user environment in
    addition to the prefix inspections"""
    install("mpileaks")
    mpileaks_spec = spack.spec.Spec("mpileaks").concretized()

    shell_out = load(shell, "mpileaks")
    load_script_file = shell_script.path_to_load_shell_script(mpileaks_spec, shell[2:])

    with open(load_script_file, "r") as f:
        shell_out = f.read()

    cmd = set_command % ("FOOBAR", "mpileaks")

    print(f"shell_out: {shell_out}")

    assert set_command % ("FOOBAR", "mpileaks") in shell_out


def test_load_first(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test with and without the --first option"""
    shell = "--bat" if sys.platform == "win32" else "--sh"
    install("libelf@0.8.12")
    install("libelf@0.8.13")

    # Now there are two versions of libelf, which should cause an error
    out = load(shell, "libelf", fail_on_error=False)
    assert "matches multiple packages" in out
    assert "Use a more specific spec" in out

    # Using --first should avoid the error condition
    load(shell, "--first", "libelf")


def test_load_fails_no_shell(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that spack load prints an error message without a shell."""
    install("mpileaks")

    out = load("mpileaks", fail_on_error=False)
    assert "To set up shell support" in out


def test_unload_fails_no_shell(
    install_mockery, mock_fetch, mock_archive, mock_packages, working_env
):
    """Test that spack unload prints an error message without a shell."""
    install("mpileaks")
    mpileaks_spec = spack.spec.Spec("mpileaks").concretized()
    os.environ[uenv.spack_loaded_hashes_var] = mpileaks_spec.dag_hash()

    out = unload("mpileaks", fail_on_error=False)
    assert "To set up shell support" in out
