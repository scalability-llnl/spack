# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import re

import pytest

import spack.config
import spack.main
import spack.modules
import spack.modules.lmod
import spack.repo
import spack.spec
import spack.store
from spack.installer import PackageInstaller

module = spack.main.SpackCommand("module")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


#: make sure module files are generated for all the tests here
@pytest.fixture(scope="module", autouse=True)
def ensure_module_files_are_there(mock_repo_path, mock_store, mock_configuration_scopes):
    """Generate module files for module tests."""
    module = spack.main.SpackCommand("module")
    with spack.store.use_store(str(mock_store)):
        with spack.config.use_configuration(*mock_configuration_scopes):
            with spack.repo.use_repositories(mock_repo_path):
                module("tcl", "refresh", "-y")


def _module_files(module_type, *specs):
    specs = [spack.spec.Spec(x).concretized() for x in specs]
    writer_cls = spack.modules.module_types[module_type]
    return [writer_cls(spec, "default").layout.filename for spec in specs]


@pytest.fixture(
    params=[
        ["rm", "doesnotexist"],  # Try to remove a non existing module
        ["find", "mpileaks"],  # Try to find a module with multiple matches
        ["find", "doesnotexist"],  # Try to find a module with no matches
        ["find", "--unknown_args"],  # Try to give an unknown argument
    ]
)
def failure_args(request):
    """A list of arguments that will cause a failure"""
    return request.param


@pytest.fixture(params=["tcl", "lmod"])
def module_type(request):
    return request.param


# TODO : test the --delete-tree option
# TODO : this requires having a separate directory for test modules
# TODO : add tests for loads and find to check the prompt format


@pytest.mark.db
def test_exit_with_failure(database, module_type, failure_args):
    with pytest.raises(spack.main.SpackCommandError):
        module(module_type, *failure_args)


@pytest.mark.db
def test_remove_and_add(database, module_type):
    """Tests adding and removing a tcl module file."""

    if module_type == "lmod":
        # TODO: Testing this with lmod requires mocking
        # TODO: the core compilers
        return

    rm_cli_args = ["rm", "-y", "mpileaks"]
    module_files = _module_files(module_type, "mpileaks")
    for item in module_files:
        assert os.path.exists(item)

    module(module_type, *rm_cli_args)
    for item in module_files:
        assert not os.path.exists(item)

    module(module_type, "refresh", "-y", "mpileaks")
    for item in module_files:
        assert os.path.exists(item)


@pytest.mark.db
@pytest.mark.parametrize("cli_args", [["libelf"], ["--full-path", "libelf"]])
def test_find(database, cli_args, module_type):
    if module_type == "lmod":
        # TODO: Testing this with lmod requires mocking
        # TODO: the core compilers
        return

    module(module_type, *(["find"] + cli_args))


@pytest.mark.db
@pytest.mark.usefixtures("database")
@pytest.mark.regression("2215")
def test_find_fails_on_multiple_matches():
    # As we installed multiple versions of mpileaks, the command will
    # fail because of multiple matches
    out = module("tcl", "find", "mpileaks", fail_on_error=False)
    assert module.returncode == 1
    assert "matches multiple packages" in out

    # Passing multiple packages from the command line also results in the
    # same failure
    out = module("tcl", "find", "mpileaks ^mpich", "libelf", fail_on_error=False)
    assert module.returncode == 1
    assert "matches multiple packages" in out


@pytest.mark.db
@pytest.mark.usefixtures("database")
@pytest.mark.regression("2570")
def test_find_fails_on_non_existing_packages():
    # Another way the command might fail is if the package does not exist
    out = module("tcl", "find", "doesnotexist", fail_on_error=False)
    assert module.returncode == 1
    assert "matches no package" in out


@pytest.mark.db
@pytest.mark.usefixtures("database")
def test_find_recursive():
    # If we call find without options it should return only one module
    out = module("tcl", "find", "mpileaks ^zmpi")
    assert len(out.split()) == 1

    # If instead we call it with the recursive option the length should
    # be greater
    out = module("tcl", "find", "-r", "mpileaks ^zmpi")
    assert len(out.split()) > 1


@pytest.mark.db
def test_find_recursive_excluded(mutable_database, module_configuration):
    module_configuration("exclude")

    module("lmod", "refresh", "-y", "--delete-tree")
    module("lmod", "find", "-r", "mpileaks ^mpich")


@pytest.mark.db
def test_loads_recursive_excluded(mutable_database, module_configuration):
    module_configuration("exclude")

    module("lmod", "refresh", "-y", "--delete-tree")
    output = module("lmod", "loads", "-r", "mpileaks ^mpich")
    lines = output.split("\n")

    assert any(re.match(r"[^#]*module load.*mpileaks", ln) for ln in lines)
    assert not any(re.match(r"[^#]module load.*callpath", ln) for ln in lines)
    assert any(re.match(r"## excluded or missing.*callpath", ln) for ln in lines)

    # TODO: currently there is no way to separate stdout and stderr when
    # invoking a SpackCommand. Supporting this requires refactoring
    # SpackCommand, or log_output, or both.
    # start_of_warning = spack.cmd.modules._missing_modules_warning[:10]
    # assert start_of_warning not in output


# Needed to make the 'module_configuration' fixture below work
writer_cls = spack.modules.lmod.LmodModulefileWriter


@pytest.mark.db
def test_setdefault_command(mutable_database, mutable_config):
    data = {
        "default": {
            "enable": ["lmod"],
            "lmod": {"core_compilers": ["clang@3.3"], "hierarchy": ["mpi"]},
        }
    }
    spack.config.set("modules", data)
    # Install two different versions of pkg-a
    other_spec, preferred = "pkg-a@1.0", "pkg-a@2.0"

    specs = [spack.spec.Spec(other_spec).concretized(), spack.spec.Spec(preferred).concretized()]
    PackageInstaller([s.package for s in specs], explicit=True, fake=True).install()

    writers = {
        preferred: writer_cls(spack.spec.Spec(preferred).concretized(), "default"),
        other_spec: writer_cls(spack.spec.Spec(other_spec).concretized(), "default"),
    }

    # Create two module files for the same software
    module("lmod", "refresh", "-y", "--delete-tree", preferred, other_spec)

    # Assert initial directory state: no link and all module files present
    link_name = os.path.join(os.path.dirname(writers[preferred].layout.filename), "default")
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert not os.path.exists(link_name)

    # Set the default to be the other spec
    module("lmod", "setdefault", other_spec)

    # Check that a link named 'default' exists, and points to the right file
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert os.path.exists(link_name) and os.path.islink(link_name)
    assert os.path.realpath(link_name) == os.path.realpath(writers[other_spec].layout.filename)

    # Reset the default to be the preferred spec
    module("lmod", "setdefault", preferred)

    # Check that a link named 'default' exists, and points to the right file
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert os.path.exists(link_name) and os.path.islink(link_name)
    assert os.path.realpath(link_name) == os.path.realpath(writers[preferred].layout.filename)
