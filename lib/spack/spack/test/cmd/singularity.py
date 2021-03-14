# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os

import pytest

import spack.cmd.singularity
from spack.error import SpackError
from spack.main import SpackCommand

singularity = SpackCommand('singularity')


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    parser = argparse.ArgumentParser()
    spack.cmd.singularity.setup_parser(parser)
    return parser


def test_recipe_centos(tmpdir, mock_packages, mock_archive, mock_fetch,
                       config, install_mockery):

    # Generate a recipe with a centos base
    with tmpdir.as_cwd():
        here = '--working_dir=%s' % os.getcwd()
        singularity('recipe', here, '--from=centos', 'perl')

    # Ensure the recipe was generated
    files = tmpdir.listdir()
    filename = tmpdir.join('Singularity')
    assert filename in files

    # Check the content
    content = filename.open().read()
    assert 'yum' in content


def test_recipe_debian(tmpdir, mock_packages, mock_archive, mock_fetch,
                       config, install_mockery):

    # Generate a recipe with a centos base
    with tmpdir.as_cwd():
        here = '--working_dir=%s' % os.getcwd()
        singularity('recipe', here, '--from=debian', 'perl')

    # Ensure the recipe was generated
    files = tmpdir.listdir()
    filename = tmpdir.join('Singularity')
    assert filename in files

    # Check the content
    content = filename.open().read()
    assert 'apt-get' in content


def test_recipe_alpine(tmpdir, mock_packages, mock_archive, mock_fetch,
                       config, install_mockery):

    # Generate a recipe with a centos base
    with tmpdir.as_cwd():
        here = '--working_dir=%s' % os.getcwd()
        singularity('recipe', here, '--from=alpine', 'perl')

    # Ensure the recipe was generated
    files = tmpdir.listdir()
    filename = tmpdir.join('Singularity')
    assert filename in files

    # Check the content
    content = filename.open().read()
    assert 'apk' in content


def test_recipe_archlinux(tmpdir, mock_packages, mock_archive, mock_fetch,
                          config, install_mockery):

    # Generate a recipe with a centos base
    with tmpdir.as_cwd():
        here = '--working_dir=%s' % os.getcwd()
        singularity('recipe', here, '--from=archlinux', 'perl')

    # Ensure the recipe was generated
    files = tmpdir.listdir()
    filename = tmpdir.join('Singularity')
    assert filename in files

    # Check the content
    content = filename.open().read()
    assert 'pacman' in content


def test_build_alpine(tmpdir, mock_packages, mock_archive, mock_fetch,
                      config, install_mockery):

    # Generate a recipe with a centos base
    with tmpdir.as_cwd():
        here = '--working_dir=%s' % os.getcwd()

        # Won't build without sudo
        with pytest.raises(SpackError):
            singularity('build', here, '--from=alpine', 'perl')
