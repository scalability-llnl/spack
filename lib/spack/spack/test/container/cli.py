# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import llnl.util.filesystem as fs

import spack.container.images
import spack.main

containerize = spack.main.SpackCommand("containerize")


def test_command(default_config, container_config_dir, capsys):
    with capsys.disabled():
        with fs.working_dir(container_config_dir):
            output = containerize()
    assert "FROM spack/ubuntu-jammy" in output


def test_listing_possible_os():
    output = containerize("--list-os")

    for expected_os in spack.container.images.all_bootstrap_os():
        assert expected_os in output


@pytest.mark.maybeslow
@pytest.mark.requires_executables("git")
def test_bootstrap_phase(minimal_configuration, config_dumper, capsys):
    minimal_configuration["spack"]["container"]["images"] = {
        "os": "amazonlinux:2",
        "spack": {"resolve_sha": False},
    }
    spack_yaml_dir = config_dumper(minimal_configuration)

    with capsys.disabled():
        with fs.working_dir(spack_yaml_dir):
            output = containerize()

    # Check for the presence of the Git commands
    assert "git init" in output
    assert "git fetch" in output
    assert "git checkout" in output
