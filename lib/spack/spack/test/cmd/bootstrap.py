# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import sys

import pytest

from llnl.path import convert_to_posix_path

import spack.bootstrap
import spack.bootstrap.core
import spack.config
import spack.environment as ev
import spack.main
import spack.mirror
import spack.spec

_bootstrap = spack.main.SpackCommand("bootstrap")


@pytest.mark.parametrize("scope", [None, "site", "system", "user"])
def test_enable_and_disable(mutable_config, scope):
    scope_args = []
    if scope:
        scope_args = ["--scope={0}".format(scope)]

    _bootstrap("enable", *scope_args)
    assert spack.config.get("bootstrap:enable", scope=scope) is True

    _bootstrap("disable", *scope_args)
    assert spack.config.get("bootstrap:enable", scope=scope) is False


@pytest.mark.parametrize("scope", [None, "site", "system", "user"])
def test_root_get_and_set(mutable_config, scope):
    scope_args, path = [], "/scratch/spack/bootstrap"
    if scope:
        scope_args = ["--scope={0}".format(scope)]

    _bootstrap("root", path, *scope_args)
    out = _bootstrap("root", *scope_args, output=str)
    if sys.platform == "win32":
        out = convert_to_posix_path(out)
    assert out.strip() == path


@pytest.mark.parametrize("scopes", [("site",), ("system", "user")])
def test_reset_in_file_scopes(mutable_config, scopes):
    # Assert files are created in the right scopes
    bootstrap_yaml_files = []
    for s in scopes:
        _bootstrap("disable", "--scope={0}".format(s))
        scope_path = spack.config.CONFIG.scopes[s].path
        bootstrap_yaml = os.path.join(scope_path, "bootstrap.yaml")
        assert os.path.exists(bootstrap_yaml)
        bootstrap_yaml_files.append(bootstrap_yaml)

    _bootstrap("reset", "-y")
    for bootstrap_yaml in bootstrap_yaml_files:
        assert not os.path.exists(bootstrap_yaml)


def test_reset_in_environment(mutable_mock_env_path, mutable_config):
    env = spack.main.SpackCommand("env")
    env("create", "bootstrap-test")
    current_environment = ev.read("bootstrap-test")

    with current_environment:
        _bootstrap("disable")
        assert spack.config.get("bootstrap:enable") is False
        _bootstrap("reset", "-y")
        # We have no default settings in tests
        assert spack.config.get("bootstrap:enable") is None

    # Check that reset didn't delete the entire file
    spack_yaml = os.path.join(current_environment.path, "spack.yaml")
    assert os.path.exists(spack_yaml)


def test_reset_in_file_scopes_overwrites_backup_files(mutable_config):
    # Create a bootstrap.yaml with some config
    _bootstrap("disable", "--scope=site")
    scope_path = spack.config.CONFIG.scopes["site"].path
    bootstrap_yaml = os.path.join(scope_path, "bootstrap.yaml")
    assert os.path.exists(bootstrap_yaml)

    # Reset the bootstrap configuration
    _bootstrap("reset", "-y")
    backup_file = bootstrap_yaml + ".bkp"
    assert not os.path.exists(bootstrap_yaml)
    assert os.path.exists(backup_file)

    # Iterate another time
    _bootstrap("disable", "--scope=site")
    assert os.path.exists(bootstrap_yaml)
    assert os.path.exists(backup_file)
    _bootstrap("reset", "-y")
    assert not os.path.exists(bootstrap_yaml)
    assert os.path.exists(backup_file)


def test_list_sources(config, capsys):
    # Get the merged list and ensure we get our defaults
    with capsys.disabled():
        output = _bootstrap("list")
    assert "github-actions" in output

    # Ask for a specific scope and check that the list of sources is empty
    with capsys.disabled():
        output = _bootstrap("list", "--scope", "user")
    assert "No method available" in output


@pytest.mark.parametrize("command,value", [("enable", True), ("disable", False)])
def test_enable_or_disable_sources(mutable_config, command, value):
    key = "bootstrap:trusted:github-actions"
    trusted = spack.config.get(key, default=None)
    assert trusted is None

    _bootstrap(command, "github-actions")
    trusted = spack.config.get(key, default=None)
    assert trusted is value


def test_enable_or_disable_fails_with_no_method(mutable_config):
    with pytest.raises(RuntimeError, match="no bootstrapping method"):
        _bootstrap("enable", "foo")


def test_enable_or_disable_fails_with_more_than_one_method(mutable_config):
    wrong_config = {
        "sources": [
            {"name": "github-actions", "metadata": "$spack/share/spack/bootstrap/github-actions"},
            {"name": "github-actions", "metadata": "$spack/share/spack/bootstrap/github-actions"},
        ],
        "trusted": {},
    }
    with spack.config.override("bootstrap", wrong_config):
        with pytest.raises(RuntimeError, match="more than one"):
            _bootstrap("enable", "github-actions")


@pytest.mark.parametrize("use_existing_dir", [True, False])
def test_add_failures_for_non_existing_files(mutable_config, tmpdir, use_existing_dir):
    metadata_dir = str(tmpdir) if use_existing_dir else "/foo/doesnotexist"
    with pytest.raises(RuntimeError, match="does not exist"):
        _bootstrap("add", "mock-mirror", metadata_dir)


def test_add_failures_for_already_existing_name(mutable_config):
    with pytest.raises(RuntimeError, match="already exist"):
        _bootstrap("add", "github-actions", "some-place")


def test_remove_failure_for_non_existing_names(mutable_config):
    with pytest.raises(RuntimeError, match="cannot find"):
        _bootstrap("remove", "mock-mirror")


def test_remove_and_add_a_source(mutable_config):
    # Check we start with a single bootstrapping source
    sources = spack.bootstrap.core.bootstrapping_sources()
    assert len(sources) == 1

    # Remove it and check the result
    _bootstrap("remove", "github-actions")
    sources = spack.bootstrap.core.bootstrapping_sources()
    assert not sources

    # Add it back and check we restored the initial state
    _bootstrap("add", "github-actions", "$spack/share/spack/bootstrap/github-actions-v0.5")
    sources = spack.bootstrap.core.bootstrapping_sources()
    assert len(sources) == 1


@pytest.mark.maybeslow
@pytest.mark.not_on_windows("Not supported on Windows (yet)")
def test_bootstrap_mirror_metadata(mutable_config, linux_os, monkeypatch, tmpdir):
    """Test that `spack bootstrap mirror` creates a folder that can be ingested by
    `spack bootstrap add`. Here we don't download data, since that would be an
    expensive operation for a unit test.
    """
    old_create = spack.mirror.create
    monkeypatch.setattr(spack.mirror, "create", lambda p, s: old_create(p, []))
    monkeypatch.setattr(spack.spec.Spec, "concretized", lambda p: p)

    # Create the mirror in a temporary folder
    compilers = [
        {
            "compiler": {
                "spec": "gcc@12.0.1",
                "operating_system": "{0.name}{0.version}".format(linux_os),
                "modules": [],
                "paths": {
                    "cc": "/usr/bin",
                    "cxx": "/usr/bin",
                    "fc": "/usr/bin",
                    "f77": "/usr/bin",
                },
            }
        }
    ]
    with spack.config.override("compilers", compilers):
        _bootstrap("mirror", str(tmpdir))

    # Register the mirror
    metadata_dir = tmpdir.join("metadata", "sources")
    _bootstrap("add", "--trust", "test-mirror", str(metadata_dir))

    assert _bootstrap.returncode == 0
    assert any(m["name"] == "test-mirror" for m in spack.bootstrap.core.bootstrapping_sources())
