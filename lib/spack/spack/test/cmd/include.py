# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.environment as ev

from spack.main import SpackCommand

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


def test_include_add_configs(tmp_path):
    """
    Test adding valid and invalid includes to an environment
    and the resulting ordering of includes is correct.
    """

    config_dir = tmp_path / "configs"
    config_dir.mkdir(parents=True, exist_ok=False)

    package_config_f = """
packages:
  {pkg}:
    externals:
    - spec: {spec}
      prefix: /usr
"""

    for idx, spec in enumerate(["abseil-cpp@20240116.2", "libelf@0.8.10", "zlib@1.3.1"]):
        (config_dir / f"{idx}").mkdir(parents=True, exist_ok=False)
        with open(config_dir / f"{idx}" / "packages.yaml", "w") as fd:
            fd.write(package_config_f.format(pkg=spec.split("@")[0], spec=spec))

    # Create a test environment
    env("create", "-d", str(config_dir / "test"))
    test = ev.read(str(config_dir / "test"))
    with test:
        add("libelf")
        # Test inserting multiple includes
        out = include("add", str(config_dir / "0"), str(config_dir / "1"))
        assert "Adding includes" in out
        assert "Invalid Paths" not in out
        assert str(config_dir / "0") in out
        assert str(config_dir / "1") in out

        # Test inserting a single path
        out = include("add", str(config_dir / "2"))
        assert "Adding includes" in out
        assert "Invalid Paths" not in out
        assert str(config_dir / "2") in out

        # Insert an invalid path should result in a warning
        out = include("add", str(config_dir / "notreal"))
        assert "Adding includes" not in out
        assert "Warning: Invalid Paths" in out
        assert str(config_dir / "notreal") in out

    test = ev.read(str(config_dir / "test"))
    # Ensure the the order of config includes matches the expected order 2, 1, 0
    # assert len(test.manifest.list_includes()) == 3
    assert str(config_dir / "2") in test.manifest.pristine_configuration["include"][0]
    assert str(config_dir / "1") in test.manifest.pristine_configuration["include"][1]
    assert str(config_dir / "0") in test.manifest.pristine_configuration["include"][2]

    test.concretize()
    hashes = test.concretized_order
    assert len(hashes) == 1
    spec = test.specs_by_hash[hashes[0]]
    # Make sure we are getting the included external
    assert spec.external()
    assert spec.satisfies("libelf@0.8.10")


def test_include_remove_configs(tmp_path):
    """Test removing includes from an activate environment"""
    config_dir = tmp_path / "configs"
    config_dir.mkdir(parents=True, exist_ok=False)

    # Need to create some placeholder directories
    (config_dir / "0").mkdir(parents=True, exist_ok=False)
    (config_dir / "2").mkdir(parents=True, exist_ok=False)

    test_env = f"""
spack:
    include:
    - {config_dir}/0
    - {config_dir}/2
"""
    (config_dir / "test").mkdir(parents=True, exist_ok=False)
    with open(str(config_dir / "test" / "spack.yaml"), "w") as fd:
        fd.write(test_env)

    test = ev.read(str(config_dir / "test"))
    with test:
        # Remove a path that does not exist in the include list
        out = include("remove", str(config_dir / "1"))
        assert "Warning: Unknown includes" in out

        # Remove a path
        include("remove", str(config_dir / "0"))

    # Verify that only the "2" include path exists
    test = ev.read(str(config_dir / "test"))
    assert len(test.manifest.pristine_configuration["include"]) == 1
    assert str(config_dir / "2") in test.manifest.pristine_configuration["include"][0]


def test_include_list_configs(tmp_path):
    """Test listing includes in an active environment"""

    config_dir = tmp_path / "configs"
    config_dir.mkdir(parents=True, exist_ok=False)

    # Need to create some placeholder directories
    (config_dir / "0").mkdir(parents=True, exist_ok=False)
    (config_dir / "2").mkdir(parents=True, exist_ok=False)

    test_env = f"""
spack:
    include:
    - {config_dir}/0
    - {config_dir}/2
"""
    (config_dir / "test").mkdir(parents=True, exist_ok=False)
    with open(str(config_dir / "test" / "spack.yaml"), "w") as fd:
        fd.write(test_env)

    test = ev.read(str(config_dir / "test"))
    with test:
        # use --expand to get the full path
        out = include("list", "--expand")
        assert "==> Included Configuration Scopes" in out
        assert str(config_dir / "0") in out
        assert str(config_dir / "2") in out
