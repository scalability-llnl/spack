# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

import pytest

import spack.container
import spack.container.images


@pytest.mark.parametrize(
    "image,spack_version,expected",
    [
        ("ubuntu:22.04", "develop", ("spack/ubuntu-jammy", "develop")),
        ("ubuntu:22.04", "0.14.0", ("spack/ubuntu-jammy", "0.14.0")),
    ],
)
def test_build_info(image, spack_version, expected):
    output = spack.container.images.build_info(image, spack_version)
    assert output == expected


@pytest.mark.parametrize("image", ["ubuntu:22.04"])
def test_package_info(image):
    pkg_manager = spack.container.images.os_package_manager_for(image)
    update, install, clean = spack.container.images.commands_for(pkg_manager)
    assert update
    assert install
    assert clean


@pytest.mark.parametrize(
    "extra_config,expected_msg",
    [
        ({"modules": {"enable": ["tcl"]}}, 'the subsection "modules" in'),
        ({"concretizer": {"unify": False}}, '"concretizer:unify" is not set to "true"'),
        (
            {"config": {"install_tree": "/some/dir"}},
            'the "config:install_tree" attribute has been set',
        ),
        ({"view": "/some/dir"}, 'the "view" attribute has been set'),
    ],
)
def test_validate(extra_config, expected_msg, minimal_configuration, config_dumper):
    minimal_configuration["spack"].update(extra_config)
    spack_yaml_dir = config_dumper(minimal_configuration)
    spack_yaml = os.path.join(spack_yaml_dir, "spack.yaml")

    with pytest.warns(UserWarning) as w:
        spack.container.validate(spack_yaml)

    # Tests are designed to raise only one warning
    assert len(w) == 1
    assert expected_msg in str(w.pop().message)
