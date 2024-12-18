# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil

import pytest

from llnl.util.filesystem import mkdirp

import spack.environment as ev
import spack.paths
import spack.spec
import spack.stage
from spack.main import SpackCommand, SpackCommandError

# Everything here uses (or can use) the mock config and database.
pytestmark = [pytest.mark.usefixtures("mutable_config", "mutable_database")]

# location prints out "locations of packages and spack directories"
location = SpackCommand("location")
env = SpackCommand("env")


@pytest.fixture
def mock_spec():
    # Make it look like the source was actually expanded.
    s = spack.spec.Spec("externaltest").concretized()
    source_path = s.package.stage.source_path
    mkdirp(source_path)
    yield s, s.package
    # Remove the spec from the mock stage area.
    shutil.rmtree(s.package.stage.path)


def test_location_first(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test with and without the --first option"""
    install = SpackCommand("install")
    install("libelf@0.8.12")
    install("libelf@0.8.13")
    # This would normally return an error without --first
    assert location("--first", "--install-dir", "libelf")


def test_location_build_dir(mock_spec):
    """Tests spack location --build-dir."""
    spec, pkg = mock_spec
    assert location("--build-dir", spec.name).strip() == pkg.stage.source_path


@pytest.mark.regression("22738")
def test_location_source_dir(mock_spec):
    """Tests spack location --source-dir."""
    spec, pkg = mock_spec
    assert location("--source-dir", spec.name).strip() == pkg.stage.source_path
    assert location(spec.name).strip() == pkg.stage.source_path


def test_location_source_dir_missing():
    """Tests spack location --source-dir with a missing source directory."""
    spec = "mpileaks"
    prefix = "==> Error: "
    expected = (
        "%sSource directory does not exist yet. Run this to create it:"
        "%s  spack stage %s" % (prefix, "\n", spec)
    )
    out = location("--source-dir", spec, fail_on_error=False).strip()
    assert out == expected


@pytest.mark.parametrize(
    "options",
    [([]), (["--source-dir", "mpileaks"]), (["--env", "missing-env"]), (["spec1", "spec2"])],
)
def test_location_cmd_error(options):
    """Ensure the proper error is raised with problematic location options."""
    with pytest.raises(SpackCommandError, match="Command exited with code 1"):
        location(*options)


def test_location_env_exists(mutable_mock_env_path):
    """Tests spack location --env <name> for an existing environment."""
    e = ev.create("example")
    e.write()
    assert location("--env", "example").strip() == e.path


def test_location_with_active_env(mutable_mock_env_path):
    """Tests spack location --env with active env"""
    e = ev.create("example")
    e.write()
    with e:
        assert location("--env").strip() == e.path


def test_location_env_flag_interference(mutable_mock_env_path):
    """
    Tests that specifying an active environment using `spack -e x location ...`
    does not interfere with the location command flags.
    """

    # create two environments
    env("create", "first_env")
    env("create", "second_env")

    global_args = ["-e", "first_env"]

    # `spack -e first_env location -e second_env` should print the env
    # path of second_env
    assert "first_env" not in location("-e", "second_env", global_args=global_args)

    # `spack -e first_env location --packages` should not print
    # the environment path of first_env.
    assert "first_env" not in location("--packages", global_args=global_args)


def test_location_env_missing():
    """Tests spack location --env."""
    missing_env_name = "missing-env"
    error = "==> Error: no such environment: '%s'" % missing_env_name
    out = location("--env", missing_env_name, fail_on_error=False).strip()
    assert out == error


@pytest.mark.db
@pytest.mark.not_on_windows("Broken on Windows")
def test_location_install_dir(mock_spec):
    """Tests spack location --install-dir."""
    spec, _ = mock_spec
    assert location("--install-dir", spec.name).strip() == spec.prefix


@pytest.mark.db
def test_location_package_dir(mock_spec):
    """Tests spack location --package-dir."""
    spec, pkg = mock_spec
    assert location("--package-dir", spec.name).strip() == pkg.package_dir


@pytest.mark.db
@pytest.mark.parametrize(
    "option,expected",
    [
        ("--module-dir", spack.paths.module_path),
        ("--packages", spack.paths.mock_packages_path),
        ("--spack-root", spack.paths.prefix),
    ],
)
def test_location_paths_options(option, expected):
    """Tests basic spack.paths location command options."""
    assert location(option).strip() == expected


@pytest.mark.parametrize(
    "specs,expected",
    [([], "You must supply a spec."), (["spec1", "spec2"], "Too many specs.  Supply only one.")],
)
def test_location_spec_errors(specs, expected):
    """Tests spack location with bad spec options."""
    error = "==> Error: %s" % expected
    assert location(*specs, fail_on_error=False).strip() == error


@pytest.mark.db
def test_location_stage_dir(mock_spec):
    """Tests spack location --stage-dir."""
    spec, pkg = mock_spec
    assert location("--stage-dir", spec.name).strip() == pkg.stage.path


@pytest.mark.db
def test_location_stages(mock_spec):
    """Tests spack location --stages."""
    assert location("--stages").strip() == spack.stage.get_stage_root()
