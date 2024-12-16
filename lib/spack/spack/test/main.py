# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import os.path
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


def test_include_cfg(mock_low_high_config, write_config_file, tmpdir):
    cfg1_path = str(tmpdir.join("include1.yaml"))
    with open(cfg1_path, "w", encoding="utf-8") as f:
        f.write(
            """\
config:
  verify_ssl: False
  dirty: True
packages:
  python:
    require:
    - spec: "@3.11:"
"""
        )

    def python_cfg(_spec):
        return f"""\
packages:
  python:
    require:
    - spec: {_spec}
"""

    def write_python_cfg(_spec, _cfg_name):
        cfg_path = str(tmpdir.join(_cfg_name))
        with open(cfg_path, "w", encoding="utf-8") as f:
            f.write(python_cfg(_spec))
        return cfg_path

    # This config will not be included
    cfg2_path = write_python_cfg("+shared", "include2.yaml")

    # The config will point to this using substitutable variables,
    # namely $os; we expect that Spack resolves these variables
    # into the actual path of the config
    this_os = spack.platforms.host().default_os
    cfg3_expanded_path = os.path.join(str(tmpdir), f"{this_os}", "include3.yaml")
    fs.mkdirp(os.path.dirname(cfg3_expanded_path))
    with open(cfg3_expanded_path, "w", encoding="utf-8") as f:
        f.write(python_cfg("+ssl"))
    cfg3_abstract_path = os.path.join(str(tmpdir), "$os", "include3.yaml")

    # This will be included unconditionally
    cfg4_path = write_python_cfg("+tk", "include4.yaml")

    # This config will not exist, and the config will explicitly
    # allow this
    cfg5_path = os.path.join(str(tmpdir), "non-existent.yaml")

    include_entries = [
        {"path": f"{cfg1_path}", "when": f'os == "{this_os}"'},
        {"path": f"{cfg2_path}", "when": "False"},
        {"path": cfg3_abstract_path},
        cfg4_path,
        {"path": cfg5_path, "optional": True},
    ]
    include_cfg = {"include": include_entries}
    write_config_file("include", include_cfg, "low")

    assert not spack.config.get("config:dirty")

    spack.main.update_config_with_includes()

    assert spack.config.get("config:dirty")
    python_reqs = spack.config.get("packages")["python"]["require"]
    req_specs = set(x["spec"] for x in python_reqs)
    assert req_specs == set(["@3.11:", "+ssl", "+tk"])
