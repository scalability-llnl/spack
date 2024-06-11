# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import pytest

import spack.cmd.env
import spack.environment as ev
import spack.environment.environment
import spack.environment.shell
import spack.error
import spack.modules
import spack.package_base
import spack.paths
import spack.repo

from spack.main import SpackCommand
from typing import List

# TODO-27021
# everything here uses the mock_env_path
pytestmark = [
    pytest.mark.usefixtures("mutable_mock_env_path", "config", "mutable_mock_repo"),
    pytest.mark.maybeslow,
    pytest.mark.not_on_windows("Envs unsupported on Windows"),
]

env = SpackCommand("env")
add = SpackCommand("add")
include = SpackCommand("include")


def create_test_envs(specs: List[str], base_name: str = "test"):
    """Create enumerated environments containing a single root spec for a list of specs"""
    envs = []
    for idx, spec in enumerate(specs):
        env_name = f"{base_name}{idx}"
        envs.append(env_name)
        env("create", env_name)
        e = ev.read(env_name)
        with e:
            add(spec)
        e.concretize()
        e.write()

    return envs


def test_include_add_configs(tmp_path):
    """Test that adds includes to an environment"""

    config_dir = tmp_path / "configs"
    config_dir.mkdir(parents=True, exist_ok=False)

    package_config_f = """
packages:
  libelf:
    externals:
    - spec: {spec}
      prefix: /usr
"""

    for idx, spec in enumerate(["abseil-cpp@20240116.2", "libelf@0.8.13", "zlib@1.3.1"]):
        (config_dir / f"{idx}").mkdir(parents=True, exist_ok=False)
        with open(config_dir / f"{idx}" / "packages.yaml", "w") as fd:
            spack.util.spack_yaml.dump(package_config_f.format(spec=spec), stream=fd)

    env("create", "test")
    test = ev.read("test")
    with test:
        add("libelf")
        include("add", str(config_dir / "0"), str(config_dir / "1"))
        include("add", str(config_dir / "2"))

    test = ev.read("test")
    # Ensure the the order of config includes matches the expected order
    assert len(test.manifest.pristine_configuration.get("include", [])) == 3
    assert str(config_dir / "2") in test.manifest.pristine_configuration["include"][0]
    assert str(config_dir / "1") in test.manifest.pristine_configuration["include"][1]
    assert str(config_dir / "0") in test.manifest.pristine_configuration["include"][2]


def test_include_remove_configs(tmp_path):
    config_dir = tmp_path / "configs"
    config_dir.mkdir(parents=True, exist_ok=False)

    (config_dir / f"0").mkdir(parents=True, exist_ok=False)

    test_env = f"""
spack:
    include:
    - {config_dir}/0
"""

    with test:
        include("remove", str(config_dir / "0"))

        with pytest.raises(spack.error.SpackError):
            include("remove", str(config_dir / "1"))

    test = ev.read("test")
    assert str(config_dir / "2") in test.manifest.pristine_configuration["include"][0]
    assert str(config_dir / "1") in test.manifest.pristine_configuration["include"][1]


def test_include_list_configs(tmp_path):

def test_env_include_concrete():
    """Test that adds concrete includes to an environment"""

    # Create some environment
    create_test_envs(["abseil-cpp", "libelf", "zlib"])

    env("create", "test")
    test = ev.read("test")
    with test:
        env("include", "--concrete", "test0", ev.root("test1"))
        env("include", "--concrete", "--prepend", "test2")
    test.write()

    test = ev.read("test")
    assert len(test.manifest.pristine_configuration.get(ev.included_concrete_name, [])) == 3
    assert ev.root("test2") == test.manifest.pristine_configuration[ev.included_concrete_name][0]
    assert ev.root("test0") == test.manifest.pristine_configuration[ev.included_concrete_name][1]
    assert ev.root("test1") == test.manifest.pristine_configuration[ev.included_concrete_name][2]

    with test:
        env("include", "--concrete", "--remove", "test0")

    test = ev.read("test")
    assert ev.root("test2") in test.manifest.pristine_configuration[ev.included_concrete_name][0]
    assert ev.root("test1") in test.manifest.pristine_configuration[ev.included_concrete_name][1]

    with test:
        env("include", "--concrete", "--remove", ev.root("test2"))

    test = ev.read("test")
    assert ev.root("test1") in test.manifest.pristine_configuration[ev.included_concrete_name][0]
