# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.util.spack_yaml as syaml


@pytest.fixture()
def minimal_configuration():
    return {
        "spack": {
            "specs": ["gromacs", "mpich", "fftw precision=float"],
            "container": {
                "format": "docker",
                "images": {"os": "ubuntu:22.04", "spack": "develop"},
            },
        }
    }


@pytest.fixture()
def config_dumper(tmpdir):
    """Function that dumps an environment config in a temporary folder."""

    def dumper(configuration):
        content = syaml.dump(configuration, default_flow_style=False)
        config_file = tmpdir / "spack.yaml"
        config_file.write(content)
        return str(tmpdir)

    return dumper


@pytest.fixture()
def container_config_dir(minimal_configuration, config_dumper):
    return config_dumper(minimal_configuration)
