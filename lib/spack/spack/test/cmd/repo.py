# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import pytest

import spack.config
import spack.environment as ev
import spack.main
from spack.main import SpackCommand

repo = spack.main.SpackCommand("repo")
env = SpackCommand("env")


def test_help_option():
    # Test 'spack repo --help' to check basic import works
    # and the command exits successfully
    with pytest.raises(SystemExit):
        repo("--help")
    assert repo.returncode in (None, 0)


def test_create_add_list_remove(mutable_config, tmpdir):
    # Create a new repository and check that the expected
    # files are there
    repo("create", str(tmpdir), "mockrepo")
    assert os.path.exists(os.path.join(str(tmpdir), "repo.yaml"))

    # Add the new repository and check it appears in the list output
    repo("add", "--scope=site", str(tmpdir))
    output = repo("list", "--scope=site", output=str)
    assert "mockrepo" in output

    # Then remove it and check it's not there
    repo("remove", "--scope=site", str(tmpdir))
    output = repo("list", "--scope=site", output=str)
    assert "mockrepo" not in output


def test_env_repo_path_vars_substitution(
    tmpdir, install_mockery, mutable_mock_env_path, monkeypatch
):
    """Test Spack correctly substitues repo paths with environment variables when creating an
    environment from a manifest file."""
    # store the repo path in an environment variable that will be used in the environment
    testrepo = "/somepath"
    monkeypatch.setenv("CUSTOM_REPO_PATH", testrepo)

    # setup environment from spack.yaml
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w", encoding="utf-8") as f:
            f.write(
                """\
spack:
  specs: []

  repos:
    - $CUSTOM_REPO_PATH
"""
            )
        # creating env from manifest file
        env("create", "test", "./spack.yaml")
        # check that repo path was correctly substituted with the environment variable
        with ev.read("test") as newenv:
            repos_specs = spack.config.get("repos", default={}, scope=newenv.scope_name)
            assert testrepo in repos_specs
