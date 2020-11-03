# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import multiprocessing

import pytest


import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config


@pytest.fixture()
def parser():
    p = argparse.ArgumentParser()
    arguments.add_common_arguments(p, ['jobs'])
    yield p
    # Cleanup the command line scope if it was set during tests
    spack.config.config.clear_caches()
    if 'command_line' in spack.config.config.scopes:
        spack.config.config.scopes['command_line'].clear()


@pytest.fixture(params=[1, 2, 4, 8, 16, 32])
def ncores(monkeypatch, request):
    """Mocks having a machine with n cores for the purpose of
    computing config:build_jobs.
    """
    def _cpu_count():
        return request.param

    # Patch multiprocessing.cpu_count() to return the value we need
    monkeypatch.setattr(multiprocessing, 'cpu_count', _cpu_count)
    # Patch the configuration parts that have been cached already
    monkeypatch.setitem(spack.config.config_defaults['config'],
                        'build_jobs', min(16, request.param))
    monkeypatch.setitem(
        spack.config.config.scopes, '_builtin',
        spack.config.InternalConfigScope(
            '_builtin', spack.config.config_defaults
        ))
    return request.param


@pytest.mark.parametrize('cli_args,requested', [
    (['-j', '24'], 24),
    # Here we report the default if we have enough cores, as the cap
    # on the available number of cores will be taken care of in the test
    ([], 16)
])
def test_setting_parallel_jobs(parser, cli_args, ncores, requested):
    expected = min(requested, ncores)
    namespace = parser.parse_args(cli_args)
    assert namespace.jobs == expected
    assert spack.config.get('config:build_jobs') == expected


def test_negative_integers_not_allowed_for_parallel_jobs(parser):
    with pytest.raises(ValueError) as exc_info:
        parser.parse_args(['-j', '-2'])

    assert 'expected a positive integer' in str(exc_info.value)


@pytest.mark.parametrize('specs,expected_variants,unexpected_variants', [
    (['coreutils', 'cflags=-O3 -g'], [], ['g']),
    (['coreutils', 'cflags=-O3', '-g'], ['g'], []),
])
@pytest.mark.regression('12951')
def test_parse_spec_flags_with_spaces(
        specs, expected_variants, unexpected_variants
):
    spec_list = spack.cmd.parse_specs(specs)
    assert len(spec_list) == 1

    s = spec_list.pop()

    assert all(x not in s.variants for x in unexpected_variants)
    assert all(x in s.variants for x in expected_variants)
