# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest
import spack.environment as ev
from spack.main import SpackCommand


# everything here uses the mock_env_path
pytestmark = pytest.mark.usefixtures(
    'mutable_mock_env_path', 'config', 'mutable_mock_repo')

env        = SpackCommand('env')
add        = SpackCommand('add')
concretize = SpackCommand('concretize')


@pytest.mark.parametrize('concretization', ['separately', 'together'])
def test_concretize_all_test_dependencies(concretization):
    """Check all test dependencies are concretized."""
    env('create', 'test')

    with ev.read('test') as e:
        e.concretization = concretization
        add('depb')
        concretize('--test', 'all')
        assert e.matching_spec('test-dependency')


@pytest.mark.parametrize('concretization', ['separately', 'together'])
def test_concretize_root_test_dependencies_not_recursive(concretization):
    """Check that test dependencies are not concretized recursively."""
    env('create', 'test')

    with ev.read('test') as e:
        e.concretization = concretization
        add('depb')
        concretize('--test', 'root')
        assert e.matching_spec('test-dependency') is None


@pytest.mark.parametrize('concretization', ['separately', 'together'])
def test_concretize_root_test_dependencies_are_concretized(concretization):
    """Check that root test dependencies are concretized."""
    env('create', 'test')

    with ev.read('test') as e:
        e.concretization = concretization
        add('a')
        add('b')
        concretize('--test', 'root')
        assert e.matching_spec('test-dependency')
