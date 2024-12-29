# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import sys

import pytest

from llnl.util.filesystem import getuid, touch

import spack
import spack.cmd.external
import spack.config
import spack.cray_manifest
import spack.detection
import spack.detection.path
import spack.repo
from spack.main import SpackCommand
from spack.spec import Spec


@pytest.fixture
def executables_found(monkeypatch):
    def _factory(result):
        def _mock_search(path_hints=None):
            return result

        monkeypatch.setattr(spack.detection.path, "executables_in_path", _mock_search)

    return _factory


def define_plat_exe(exe):
    if sys.platform == "win32":
        exe += ".bat"
    return exe


def test_find_external_single_package(mock_executable):
    cmake_path = mock_executable("cmake", output="echo cmake version 1.foo")
    search_dir = cmake_path.parent.parent

    specs_by_package = spack.detection.by_path(["cmake"], path_hints=[str(search_dir)])

    assert len(specs_by_package) == 1 and "cmake" in specs_by_package
    detected_spec = specs_by_package["cmake"]
    assert len(detected_spec) == 1 and detected_spec[0] == Spec("cmake@1.foo")


def test_find_external_two_instances_same_package(mock_executable):
    # Each of these cmake instances is created in a different prefix
    # In Windows, quoted strings are echo'd with quotes includes
    # we need to avoid that for proper regex.
    cmake1 = mock_executable("cmake", output="echo cmake version 1.foo", subdir=("base1", "bin"))
    cmake2 = mock_executable("cmake", output="echo cmake version 3.17.2", subdir=("base2", "bin"))
    search_paths = [str(cmake1.parent.parent), str(cmake2.parent.parent)]

    finder = spack.detection.path.ExecutablesFinder()
    detected_specs = finder.find(
        pkg_name="cmake", initial_guess=search_paths, repository=spack.repo.PATH
    )

    assert len(detected_specs) == 2
    spec_to_path = {s: s.external_path for s in detected_specs}
    assert spec_to_path[Spec("cmake@1.foo")] == (
        spack.detection.executable_prefix(str(cmake1.parent))
    ), spec_to_path
    assert spec_to_path[Spec("cmake@3.17.2")] == (
        spack.detection.executable_prefix(str(cmake2.parent))
    )


def test_find_external_update_config(mutable_config):
    entries = [
        Spec.from_detection("cmake@1.foo", external_path="/x/y1"),
        Spec.from_detection("cmake@3.17.2", external_path="/x/y2"),
    ]
    pkg_to_entries = {"cmake": entries}

    scope = spack.config.default_modify_scope("packages")
    spack.detection.update_configuration(pkg_to_entries, scope=scope, buildable=True)

    pkgs_cfg = spack.config.get("packages")
    cmake_cfg = pkgs_cfg["cmake"]
    cmake_externals = cmake_cfg["externals"]

    assert {"spec": "cmake@1.foo", "prefix": "/x/y1"} in cmake_externals
    assert {"spec": "cmake@3.17.2", "prefix": "/x/y2"} in cmake_externals


def test_get_executables(working_env, mock_executable):
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    path_to_exe = spack.detection.executables_in_path([os.path.dirname(cmake_path1)])
    cmake_exe = define_plat_exe("cmake")
    assert path_to_exe[str(cmake_path1)] == cmake_exe


external = SpackCommand("external")


# TODO: this test should be made to work, but in the meantime it is
# causing intermittent (spurious) CI failures on all PRs
@pytest.mark.not_on_windows("Test fails intermittently on Windows")
def test_find_external_cmd_not_buildable(mutable_config, working_env, mock_executable):
    """When the user invokes 'spack external find --not-buildable', the config
    for any package where Spack finds an external version should be marked as
    not buildable.
    """
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    os.environ["PATH"] = os.pathsep.join([os.path.dirname(cmake_path1)])
    external("find", "--not-buildable", "cmake")
    pkgs_cfg = spack.config.get("packages")
    assert "cmake" in pkgs_cfg
    assert not pkgs_cfg["cmake"]["buildable"]


@pytest.mark.parametrize(
    "names,tags,exclude,expected",
    [
        # find -all
        (
            None,
            ["detectable"],
            [],
            [
                "builtin.mock.find-externals1",
                "builtin.mock.gcc",
                "builtin.mock.llvm",
                "builtin.mock.intel-oneapi-compilers",
            ],
        ),
        # find --all --exclude find-externals1
        (
            None,
            ["detectable"],
            ["builtin.mock.find-externals1"],
            ["builtin.mock.gcc", "builtin.mock.llvm", "builtin.mock.intel-oneapi-compilers"],
        ),
        (
            None,
            ["detectable"],
            ["find-externals1"],
            ["builtin.mock.gcc", "builtin.mock.llvm", "builtin.mock.intel-oneapi-compilers"],
        ),
        # find cmake (and cmake is not detectable)
        (["cmake"], ["detectable"], [], []),
    ],
)
def test_package_selection(names, tags, exclude, expected, mutable_mock_repo):
    """Tests various cases of selecting packages"""
    # In the mock repo we only have 'find-externals1' that is detectable
    result = spack.cmd.external.packages_to_search_for(names=names, tags=tags, exclude=exclude)
    assert set(result) == set(expected)


def test_find_external_no_manifest(mutable_config, working_env, mutable_mock_repo, monkeypatch):
    """The user runs 'spack external find'; the default path for storing
    manifest files does not exist. Ensure that the command does not
    fail.
    """
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(
        spack.cray_manifest, "default_path", os.path.join("a", "path", "that", "doesnt", "exist")
    )
    external("find")


def test_find_external_empty_default_manifest_dir(
    mutable_config, working_env, mutable_mock_repo, tmpdir, monkeypatch
):
    """The user runs 'spack external find'; the default path for storing
    manifest files exists but is empty. Ensure that the command does not
    fail.
    """
    empty_manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(spack.cray_manifest, "default_path", empty_manifest_dir)
    external("find")


@pytest.mark.not_on_windows("Can't chmod on Windows")
@pytest.mark.skipif(getuid() == 0, reason="user is root")
def test_find_external_manifest_with_bad_permissions(
    mutable_config, working_env, mutable_mock_repo, tmpdir, monkeypatch
):
    """The user runs 'spack external find'; the default path for storing
    manifest files exists but with insufficient permissions. Check that
    the command does not fail.
    """
    test_manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    test_manifest_file_path = os.path.join(test_manifest_dir, "badperms.json")
    touch(test_manifest_file_path)
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(spack.cray_manifest, "default_path", test_manifest_dir)
    try:
        os.chmod(test_manifest_file_path, 0)
        output = external("find")
        assert "insufficient permissions" in output
        assert "Skipping manifest and continuing" in output
    finally:
        os.chmod(test_manifest_file_path, 0o700)


def test_find_external_manifest_failure(mutable_config, mutable_mock_repo, tmpdir, monkeypatch):
    """The user runs 'spack external find'; the manifest parsing fails with
    some exception. Ensure that the command still succeeds (i.e. moves on
    to other external detection mechanisms).
    """
    # First, create an empty manifest file (without a file to read, the
    # manifest parsing is skipped)
    test_manifest_dir = str(tmpdir.mkdir("manifest_dir"))
    test_manifest_file_path = os.path.join(test_manifest_dir, "test.json")
    touch(test_manifest_file_path)

    def fail():
        raise Exception()

    monkeypatch.setattr(spack.cmd.external, "_collect_and_consume_cray_manifest_files", fail)
    monkeypatch.setenv("PATH", "")
    output = external("find")
    assert "Skipping manifest and continuing" in output


def test_find_external_merge(mutable_config, mutable_mock_repo, tmp_path):
    """Checks that 'spack find external' doesn't overwrite an existing spec in packages.yaml."""
    pkgs_cfg_init = {
        "find-externals1": {
            "externals": [{"spec": "find-externals1@1.1", "prefix": "/preexisting-prefix"}],
            "buildable": False,
        }
    }

    mutable_config.update_config("packages", pkgs_cfg_init)
    entries = [
        Spec.from_detection("find-externals1@1.1", external_path="/x/y1"),
        Spec.from_detection("find-externals1@1.2", external_path="/x/y2"),
    ]
    pkg_to_entries = {"find-externals1": entries}
    scope = spack.config.default_modify_scope("packages")
    spack.detection.update_configuration(pkg_to_entries, scope=scope, buildable=True)

    pkgs_cfg = spack.config.get("packages")
    pkg_cfg = pkgs_cfg["find-externals1"]
    pkg_externals = pkg_cfg["externals"]

    assert {"spec": "find-externals1@1.1", "prefix": "/preexisting-prefix"} in pkg_externals
    assert {"spec": "find-externals1@1.2", "prefix": "/x/y2"} in pkg_externals


def test_list_detectable_packages(mutable_config, mutable_mock_repo):
    external("list")
    assert external.returncode == 0


def test_overriding_prefix(mock_executable, mutable_config, monkeypatch):
    gcc_exe = mock_executable("gcc", output="echo 4.2.1")
    search_dir = gcc_exe.parent

    @classmethod
    def _determine_variants(cls, exes, version_str):
        return "languages=c", {"prefix": "/opt/gcc/bin", "compilers": {"c": exes[0]}}

    gcc_cls = spack.repo.PATH.get_pkg_class("gcc")
    monkeypatch.setattr(gcc_cls, "determine_variants", _determine_variants)

    finder = spack.detection.path.ExecutablesFinder()
    detected_specs = finder.find(
        pkg_name="gcc", initial_guess=[str(search_dir)], repository=spack.repo.PATH
    )

    assert len(detected_specs) == 1

    gcc = detected_specs[0]
    assert gcc.name == "gcc"
    assert gcc.external_path == os.path.sep + os.path.join("opt", "gcc", "bin")


@pytest.mark.not_on_windows("Fails spuriously on Windows")
def test_new_entries_are_reported_correctly(mock_executable, mutable_config, monkeypatch):
    # Prepare an environment to detect a fake gcc
    gcc_exe = mock_executable("gcc", output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv("PATH", prefix)

    # The first run will find and add the external gcc
    output = external("find", "gcc")
    assert "The following specs have been" in output

    # The second run should report that no new external
    # has been found
    output = external("find", "gcc")
    assert "No new external packages detected" in output


@pytest.mark.parametrize("command_args", [("-t", "build-tools"), ("-t", "build-tools", "cmake")])
def test_use_tags_for_detection(command_args, mock_executable, mutable_config, monkeypatch):
    # Prepare an environment to detect a fake cmake
    cmake_exe = mock_executable("cmake", output="echo cmake version 3.19.1")
    prefix = os.path.dirname(cmake_exe)
    monkeypatch.setenv("PATH", prefix)

    openssl_exe = mock_executable("openssl", output="OpenSSL 2.8.3")
    prefix = os.path.dirname(openssl_exe)
    monkeypatch.setenv("PATH", prefix)

    # Test that we detect specs
    output = external("find", *command_args)
    assert "The following specs have been" in output
    assert "cmake" in output
    assert "openssl" not in output


@pytest.mark.regression("38733")
@pytest.mark.not_on_windows("the test uses bash scripts")
def test_failures_in_scanning_do_not_result_in_an_error(
    mock_executable, monkeypatch, mutable_config
):
    """Tests that scanning paths with wrong permissions, won't cause `external find` to error."""
    cmake_exe1 = mock_executable(
        "cmake", output="echo cmake version 3.19.1", subdir=("first", "bin")
    )
    cmake_exe2 = mock_executable(
        "cmake", output="echo cmake version 3.23.3", subdir=("second", "bin")
    )

    # Remove access from the first directory executable
    cmake_exe1.parent.chmod(0o600)

    value = os.pathsep.join([str(cmake_exe1.parent), str(cmake_exe2.parent)])
    monkeypatch.setenv("PATH", value)

    output = external("find", "cmake")
    assert external.returncode == 0
    assert "The following specs have been" in output
    assert "cmake" in output
    assert "3.23.3" in output
    assert "3.19.1" not in output


def test_detect_virtuals(mock_executable, mutable_config, monkeypatch):
    """Test whether external find --not-buildable sets virtuals as non-buildable (unless user
    config sets them to buildable)"""
    mpich = mock_executable("mpichversion", output="echo MPICH Version:    4.0.2")
    prefix = os.path.dirname(mpich)
    external("find", "--path", prefix, "--not-buildable", "mpich")

    # Check that mpich was correctly detected
    mpich = mutable_config.get("packages:mpich")
    assert mpich["buildable"] is False
    assert Spec(mpich["externals"][0]["spec"]).satisfies("mpich@4.0.2")

    # Check that the virtual package mpi was marked as non-buildable
    assert mutable_config.get("packages:mpi:buildable") is False

    # Delete the mpich entry, and set mpi explicitly to buildable
    mutable_config.set("packages:mpich", {})
    mutable_config.set("packages:mpi:buildable", True)

    # Run the detection again
    external("find", "--path", prefix, "--not-buildable", "mpich")

    # Check that the mpi:buildable entry was not overwritten
    assert mutable_config.get("packages:mpi:buildable") is True
