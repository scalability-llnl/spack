# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest


import spack.container.writers as writers


def test_manifest(minimal_configuration):
    writer = writers.create(minimal_configuration)
    manifest_str = writer.manifest
    for line in manifest_str.split('\n'):
        assert 'echo' in line


def test_build_and_run_images(minimal_configuration):
    writer = writers.create(minimal_configuration)

    # Test the output of run property
    run = writer.run
    assert run.image == 'ubuntu:18.04'

    # Test the output of the build property
    build = writer.build
    assert build.image == 'spack/ubuntu-bionic:latest'


def test_packages(minimal_configuration):
    # In this minimal configuration we don't have packages
    writer = writers.create(minimal_configuration)
    assert writer.os_packages_build is None
    assert writer.os_packages_final is None

    # If we add them a list should be returned
    pkgs = ['libgomp1']
    minimal_configuration['spack']['container']['os_packages'] = {
        'final': pkgs
    }
    writer = writers.create(minimal_configuration)
    p = writer.os_packages_final
    assert p.update
    assert p.install
    assert p.clean
    assert p.list == pkgs


def test_ensure_render_works(minimal_configuration, default_config):
    # Here we just want to ensure that nothing is raised
    writer = writers.create(minimal_configuration)
    writer()


def test_strip_is_set_from_config(minimal_configuration):
    writer = writers.create(minimal_configuration)
    assert writer.strip is True

    minimal_configuration['spack']['container']['strip'] = False
    writer = writers.create(minimal_configuration)
    assert writer.strip is False


def test_extra_instructions_is_set_from_config(minimal_configuration):
    writer = writers.create(minimal_configuration)
    assert writer.extra_instructions == (None, None)

    test_line = 'RUN echo Hello world!'
    e = minimal_configuration['spack']['container']
    e['extra_instructions'] = {}
    e['extra_instructions']['build'] = test_line
    writer = writers.create(minimal_configuration)
    assert writer.extra_instructions == (test_line, None)

    e['extra_instructions']['final'] = test_line
    del e['extra_instructions']['build']
    writer = writers.create(minimal_configuration)
    assert writer.extra_instructions == (None, test_line)


def test_custom_base_images(minimal_configuration):
    """Test setting custom base images from configuration file"""
    minimal_configuration['spack']['container']['images'] = {
        'build': 'custom-build:latest',
        'final': 'custom-final:latest'
    }
    writer = writers.create(minimal_configuration)

    assert writer.bootstrap.image is None
    assert writer.build.image == 'custom-build:latest'
    assert writer.run.image == 'custom-final:latest'


@pytest.mark.parametrize('images_cfg,expected', [
    ({'os': 'amazonlinux:2', 'spack': 'develop'}, {
        'bootstrap_image': 'amazonlinux:2',
        'build_image': 'bootstrap',
        'final_image': 'amazonlinux:2'
    })
])
def test_base_images_with_bootstrap(
        minimal_configuration, images_cfg, expected
):
    """Check that base images are computed correctly when a
    bootstrap phase is present
    """
    minimal_configuration['spack']['container']['images'] = images_cfg
    writer = writers.create(minimal_configuration)

    for property_name, value in expected.items():
        assert getattr(writer, property_name) == value


def test_error_message_invalid_os(minimal_configuration):
    minimal_configuration['spack']['container']['images']['os'] = 'invalid:1'
    with pytest.raises(ValueError, match='invalid operating system'):
        writers.create(minimal_configuration)
