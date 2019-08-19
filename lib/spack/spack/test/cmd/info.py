# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import pytest
import spack.cmd.info

from spack.main import SpackCommand

info = SpackCommand('info')


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    prs = argparse.ArgumentParser()
    spack.cmd.info.setup_parser(prs)
    return prs


@pytest.fixture()
def info_lines():
    lines = []
    return lines


@pytest.fixture()
def mock_print(monkeypatch, info_lines):

    def _print(*args):
        info_lines.extend(args)

    monkeypatch.setattr(spack.cmd.info.color, 'cprint', _print, raising=False)


@pytest.mark.parametrize('pkg', [
    'openmpi',
    'trilinos',
    'boost',
    'python',
    'dealii'
])
def test_it_just_runs(pkg):
    info(pkg)


@pytest.mark.parametrize('pkg_query', [
    'hdf5',
    'cloverleaf3d',
    'trilinos'
])
@pytest.mark.usefixtures('mock_print')
def test_info_fields(pkg_query, parser, info_lines):

    expected_fields = (
        'Description:',
        'Caveats:',
        'Homepage:',
        'Safe versions:',
        'Variants:',
        'Installation Phases:',
        'Virtual Packages:',
        'Tags:'
    )

    args = parser.parse_args([pkg_query])
    spack.cmd.info.info(parser, args)

    for text in expected_fields:
        match = [x for x in info_lines if text in x]
        assert match
