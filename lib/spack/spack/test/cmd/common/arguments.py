# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import pytest

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config
import spack.environment as ev


@pytest.fixture()
def job_parser():
    # --jobs needs to write to a command_line config scope, so this is the only
    # scope we create.
    p = argparse.ArgumentParser()
    arguments.add_common_arguments(p, ['jobs'])
    scopes = [spack.config.InternalConfigScope('command_line', {'config': {}})]

    with spack.config.use_configuration(*scopes):
        yield p


def test_setting_jobs_flag(job_parser):
    namespace = job_parser.parse_args(['-j', '24'])
    assert namespace.jobs == 24
    assert spack.config.get('config:build_jobs', scope='command_line') == 24


def test_omitted_job_flag(job_parser):
    namespace = job_parser.parse_args([])
    assert namespace.jobs is None
    assert spack.config.get('config:build_jobs') is None


def test_negative_integers_not_allowed_for_parallel_jobs(job_parser):
    with pytest.raises(ValueError) as exc_info:
        job_parser.parse_args(['-j', '-2'])

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


@pytest.mark.usefixtures('config')
def test_match_spec_env(mock_packages, mutable_mock_env_path):
    """
    Concretize a spec with non-default options in an environment. Make
    sure that when we ask for a matching spec when the environment is
    active that we get the instance concretized in the environment.
    """
    # Initial sanity check: we are planning on choosing a non-default
    # value, so make sure that is in fact not the default.
    check_defaults = spack.cmd.parse_specs(['a'], concretize=True)[0]
    assert not check_defaults.satisfies('foobar=baz')

    e = ev.create('test')
    e.add('a foobar=baz')
    e.concretize()
    with e:
        env_spec = spack.cmd.matching_spec_from_env(
            spack.cmd.parse_specs(['a'])[0])
        assert env_spec.satisfies('foobar=baz')
        assert env_spec.concrete


@pytest.mark.usefixtures('config')
def test_multiple_env_match_raises_error(mock_packages, mutable_mock_env_path):
    e = ev.create('test')
    e.add('a foobar=baz')
    e.add('a foobar=fee')
    e.concretize()
    with e:
        with pytest.raises(
                spack.environment.SpackEnvironmentError) as exc_info:

            spack.cmd.matching_spec_from_env(spack.cmd.parse_specs(['a'])[0])

    assert 'matches multiple specs' in exc_info.value.message
