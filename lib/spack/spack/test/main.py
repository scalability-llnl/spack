# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import llnl.util.filesystem as fs

import spack
import spack.config
import spack.environment as ev
import spack.error
import spack.main
import spack.paths
import spack.util.executable as exe
import spack.util.git

pytestmark = pytest.mark.not_on_windows(
    "Test functionality supported but tests are failing on Win"
)


def test_version_git_nonsense_output(tmpdir, working_env, monkeypatch):
    git = str(tmpdir.join("git"))
    with open(git, "w", encoding="utf-8") as f:
        f.write(
            """#!/bin/sh
echo --|not a hash|----
"""
        )
    fs.set_executable(git)

    monkeypatch.setattr(spack.util.git, "git", lambda: exe.which(git))
    assert spack.spack_version == spack.get_version()


def test_version_git_fails(tmpdir, working_env, monkeypatch):
    git = str(tmpdir.join("git"))
    with open(git, "w", encoding="utf-8") as f:
        f.write(
            """#!/bin/sh
echo 26552533be04e83e66be2c28e0eb5011cb54e8fa
exit 1
"""
        )
    fs.set_executable(git)

    monkeypatch.setattr(spack.util.git, "git", lambda: exe.which(git))
    assert spack.spack_version == spack.get_version()


def test_git_sha_output(tmpdir, working_env, monkeypatch):
    git = str(tmpdir.join("git"))
    sha = "26552533be04e83e66be2c28e0eb5011cb54e8fa"
    with open(git, "w", encoding="utf-8") as f:
        f.write(
            """#!/bin/sh
echo {0}
""".format(
                sha
            )
        )
    fs.set_executable(git)

    monkeypatch.setattr(spack.util.git, "git", lambda: exe.which(git))
    expected = "{0} ({1})".format(spack.spack_version, sha)
    assert expected == spack.get_version()


def test_get_version_no_repo(tmpdir, monkeypatch):
    monkeypatch.setattr(spack.paths, "prefix", str(tmpdir))
    assert spack.spack_version == spack.get_version()


def test_get_version_no_git(tmpdir, working_env, monkeypatch):
    monkeypatch.setattr(spack.util.git, "git", lambda: None)
    assert spack.spack_version == spack.get_version()


def test_main_calls_get_version(tmpdir, capsys, working_env, monkeypatch):
    # act like git is not found in the PATH
    monkeypatch.setattr(spack.util.git, "git", lambda: None)

    # make sure we get a bare version (without commit) when this happens
    spack.main.main(["-V"])
    out, err = capsys.readouterr()
    assert spack.spack_version == out.strip()


def test_get_version_bad_git(tmpdir, working_env, monkeypatch):
    bad_git = str(tmpdir.join("git"))
    with open(bad_git, "w", encoding="utf-8") as f:
        f.write(
            """#!/bin/sh
exit 1
"""
        )
    fs.set_executable(bad_git)

    monkeypatch.setattr(spack.util.git, "git", lambda: exe.which(bad_git))
    assert spack.spack_version == spack.get_version()


def test_bad_command_line_scopes(tmp_path, config):
    cfg = spack.config.Configuration()
    file_path = tmp_path / "file_instead_of_dir"
    non_existing_path = tmp_path / "non_existing_dir"

    file_path.write_text("")

    with pytest.raises(spack.error.ConfigError):
        spack.main.add_command_line_scopes(cfg, [str(file_path)])

    with pytest.raises(spack.error.ConfigError):
        spack.main.add_command_line_scopes(cfg, [str(non_existing_path)])


def test_add_command_line_scopes(tmpdir, mutable_config):
    config_yaml = str(tmpdir.join("config.yaml"))
    with open(config_yaml, "w", encoding="utf-8") as f:
        f.write(
            """\
config:
    verify_ssl: False
    dirty: False
"""
        )

    spack.main.add_command_line_scopes(mutable_config, [str(tmpdir)])
    assert mutable_config.get("config:verify_ssl") is False
    assert mutable_config.get("config:dirty") is False


def test_add_command_line_scope_env(tmp_path, mutable_mock_env_path):
    """Test whether --config-scope <env> works, either by name or path."""
    managed_env = ev.create("example").manifest_path

    with open(managed_env, "w", encoding="utf-8") as f:
        f.write(
            """\
spack:
  config:
    install_tree:
      root: /tmp/first
"""
        )

    with open(tmp_path / "spack.yaml", "w", encoding="utf-8") as f:
        f.write(
            """\
spack:
  config:
    install_tree:
      root: /tmp/second
"""
        )

    config = spack.config.Configuration()
    spack.main.add_command_line_scopes(config, ["example", str(tmp_path)])
    assert len(config.scopes) == 2
    assert config.get("config:install_tree:root") == "/tmp/second"

    config = spack.config.Configuration()
    spack.main.add_command_line_scopes(config, [str(tmp_path), "example"])
    assert len(config.scopes) == 2
    assert config.get("config:install_tree:root") == "/tmp/first"

    assert ev.active_environment() is None  # shouldn't cause an environment to be activated
