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
concretize = SpackCommand("concretize")


def test_include_config_add(tmp_path):
    """
    Test adding valid and invalid includes to an environment
    and the resulting ordering of includes is correct.
    """

    config_dir = tmp_path / "configs"
    config_dir.mkdir(parents=True, exist_ok=False)

    package_config_f = """
packages:
  {pkg}:
    buildable: False
    externals:
    - spec: {spec}
      prefix: {prefix}
"""

    for idx, spec in enumerate(["abseil-cpp@20240116.2", "libelf@0.8.10", "zlib@1.3.1"]):
        (config_dir / f"{idx}").mkdir(parents=True, exist_ok=False)
        with open(config_dir / f"{idx}" / "packages.yaml", "w") as fd:
            fd.write(
                package_config_f.format(pkg=spec.split("@")[0], spec=spec, prefix=str(tmp_path))
            )

    # Create a test environment
    env("create", "-d", str(config_dir / "test"))
    test = ev.read(str(config_dir / "test"))
    with test:
        add("libelf@0.8.10")
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


def test_include_config_remove(tmp_path):
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


def test_include_config_list(tmp_path):
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
        assert str(config_dir / "0") in out
        assert str(config_dir / "2") in out


def test_include_concrete_add(tmp_path):
    """Test listing includes in an active environment"""

    test_env_template = """
spack:
    specs:
    - {0}
"""

    # Create a B environment
    env_dir = tmp_path / "env"
    env_dir.mkdir(parents=True, exist_ok=False)

    def create_test_env(name, config):
        (env_dir / name).mkdir(parents=True, exist_ok=False)
        with open(str(env_dir / name / "spack.yaml"), "w") as fd:
            fd.write(config)

        e = ev.read(str(env_dir / name))
        with e:
            concretize()

        e = ev.read(str(env_dir / name))
        return e.specs_by_hash, e

    bspecs, _ = create_test_env("B", test_env_template.format("b"))
    especs, _ = create_test_env("E", test_env_template.format("e"))

    # Create a A environment that includes B and E
    _, testa = create_test_env("A", test_env_template.format("a"))
    with testa:
        include("--concrete", "add", str(env_dir / "B"))
        include("--concrete", "add", str(env_dir / "E"))
        concretize("-f")

    testa = ev.read(str(env_dir / "A"))
    assert str(env_dir / "B") in testa.manifest.pristine_configuration["include_concrete"]
    assert str(env_dir / "E") in testa.manifest.pristine_configuration["include_concrete"]
    # TODO: Add checks for reuse of included concrete specs once that works


def test_include_concrete_remove(tmp_path):
    """Test listing includes in an active environment"""

    test_env_template = """
spack:
    specs:
    - {0}
"""

    # Create a B environment
    env_dir = tmp_path / "env"
    env_dir.mkdir(parents=True, exist_ok=False)

    def create_test_env(name, config):
        (env_dir / name).mkdir(parents=True, exist_ok=False)
        with open(str(env_dir / name / "spack.yaml"), "w") as fd:
            fd.write(config)

        e = ev.read(str(env_dir / name))
        with e:
            concretize()

        e = ev.read(str(env_dir / name))
        return e.specs_by_hash, e

    bspecs, _ = create_test_env("B", test_env_template.format("b"))
    especs, _ = create_test_env("E", test_env_template.format("e"))

    # Create a A environment that includes B and E
    _, testa = create_test_env("A", test_env_template.format("a"))
    with testa:
        include("--concrete", "add", str(env_dir / "B"))
        include("--concrete", "add", str(env_dir / "E"))
        include("--concrete", "remove", str(env_dir / "B"))
        concretize("-f")

    testa = ev.read(str(env_dir / "A"))
    assert str(env_dir / "B") not in testa.manifest.pristine_configuration["include_concrete"]
    assert str(env_dir / "E") in testa.manifest.pristine_configuration["include_concrete"]
    # TODO: Add checks for reuse of included concrete specs once that works


def test_include_concrete_list(tmp_path):
    """Test listing includes in an active environment"""

    test_env_template = """
spack:
    specs:
    - {0}
"""

    # Create a B environment
    env_dir = tmp_path / "env"
    env_dir.mkdir(parents=True, exist_ok=False)

    # Make a configs dir
    (env_dir / "configs").mkdir(parents=True, exist_ok=False)

    def create_test_env(name, config):
        (env_dir / name).mkdir(parents=True, exist_ok=False)
        with open(str(env_dir / name / "spack.yaml"), "w") as fd:
            fd.write(config)

        e = ev.read(str(env_dir / name))
        with e:
            concretize()

        e = ev.read(str(env_dir / name))
        return e.specs_by_hash, e

    bspecs, _ = create_test_env("B", test_env_template.format("b"))
    especs, _ = create_test_env("E", test_env_template.format("e"))

    # Create a A environment that includes B and E
    _, testa = create_test_env("A", test_env_template.format("a"))
    with testa:
        include("--concrete", "add", str(env_dir / "B"))
        include("--concrete", "add", str(env_dir / "E"))
        include("add", str(env_dir / "configs"))

        out = include("--concrete", "list", "--expand")
        # Ensure all of the include concrete dirs are listed
        assert str(env_dir / "B") in out
        assert str(env_dir / "E") in out

        # Ensure the include configs dir is not listed
        assert str(env_dir / "configs") not in out
