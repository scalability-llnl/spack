# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import pytest

import spack.container.writers as writers


def test_manifest(minimal_configuration):
    writer = writers.create(minimal_configuration)
    manifest_str = writer.manifest
    for line in manifest_str.split("\n"):
        assert "echo" in line


def test_build_and_run_images(minimal_configuration):
    writer = writers.create(minimal_configuration)

    # Test the output of run property
    run = writer.run
    assert run.image == "ubuntu:22.04"

    # Test the output of the build property
    build = writer.build
    assert build.image == "spack/ubuntu-jammy:develop"


def test_packages(minimal_configuration):
    # In this minimal configuration we don't have packages
    writer = writers.create(minimal_configuration)
    assert writer.os_packages_build is None
    assert writer.os_packages_final is None

    # If we add them a list should be returned
    pkgs = ["libgomp1"]
    minimal_configuration["spack"]["container"]["os_packages"] = {"final": pkgs}
    writer = writers.create(minimal_configuration)
    p = writer.os_packages_final
    assert p.update
    assert p.install
    assert p.clean
    assert p.list == pkgs


def test_container_os_packages_command(minimal_configuration):
    # In this minimal configuration we don't have packages
    writer = writers.create(minimal_configuration)
    assert writer.os_packages_build is None
    assert writer.os_packages_final is None

    # If we add them a list should be returned
    minimal_configuration["spack"]["container"]["images"] = {
        "build": "custom-build:latest",
        "final": "custom-final:latest",
    }
    minimal_configuration["spack"]["container"]["os_packages"] = {
        "command": "zypper",
        "final": ["libgomp1"],
    }
    writer = writers.create(minimal_configuration)
    p = writer.os_packages_final
    assert "zypper update -y" in p.update
    assert "zypper install -y" in p.install
    assert "zypper clean -a" in p.clean


def test_ensure_render_works(minimal_configuration, default_config):
    # Here we just want to ensure that nothing is raised
    writer = writers.create(minimal_configuration)
    writer()


def test_strip_is_set_from_config(minimal_configuration):
    writer = writers.create(minimal_configuration)
    assert writer.strip is True

    minimal_configuration["spack"]["container"]["strip"] = False
    writer = writers.create(minimal_configuration)
    assert writer.strip is False


def test_custom_base_images(minimal_configuration):
    """Test setting custom base images from configuration file"""
    minimal_configuration["spack"]["container"]["images"] = {
        "build": "custom-build:latest",
        "final": "custom-final:latest",
    }
    writer = writers.create(minimal_configuration)

    assert writer.bootstrap.image is None
    assert writer.build.image == "custom-build:latest"
    assert writer.run.image == "custom-final:latest"


@pytest.mark.parametrize(
    "images_cfg,expected",
    [
        (
            {"os": "amazonlinux:2", "spack": "develop"},
            {
                "bootstrap_image": "amazonlinux:2",
                "build_image": "bootstrap",
                "final_image": "amazonlinux:2",
            },
        )
    ],
)
def test_base_images_with_bootstrap(minimal_configuration, images_cfg, expected):
    """Check that base images are computed correctly when a
    bootstrap phase is present
    """
    minimal_configuration["spack"]["container"]["images"] = images_cfg
    writer = writers.create(minimal_configuration)

    for property_name, value in expected.items():
        assert getattr(writer, property_name) == value


def test_error_message_invalid_os(minimal_configuration):
    minimal_configuration["spack"]["container"]["images"]["os"] = "invalid:1"
    with pytest.raises(ValueError, match="invalid operating system"):
        writers.create(minimal_configuration)


@pytest.mark.regression("34629,18030")
def test_not_stripping_all_symbols(minimal_configuration):
    """Tests that we are not stripping all symbols, so that libraries can still be
    used for linking.
    """
    minimal_configuration["spack"]["container"]["strip"] = True
    content = writers.create(minimal_configuration)()
    assert "xargs strip" in content
    assert "xargs strip -s" not in content


@pytest.mark.regression("22341")
def test_using_single_quotes_in_dockerfiles(minimal_configuration):
    """Tests that Dockerfiles written by Spack use single quotes in manifest, to avoid issues
    with shell substitution. This may happen e.g. when users have "definitions:" they want to
    expand in dockerfiles.
    """
    manifest_in_docker = writers.create(minimal_configuration).manifest
    assert not re.search(r"echo\s*\"", manifest_in_docker, flags=re.MULTILINE)
    assert re.search(r"echo\s*'", manifest_in_docker)
