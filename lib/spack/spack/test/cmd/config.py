# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from llnl.util.filesystem import mkdirp

import spack.config
import spack.environment as ev
from spack.main import SpackCommand

config = SpackCommand('config')


def test_get_config_scope(mock_config):
    assert config('get', 'compilers').strip() == 'compilers: {}'


def test_get_config_scope_merged(mock_config):
    low_path = mock_config.scopes['low'].path
    high_path = mock_config.scopes['high'].path

    mkdirp(low_path)
    mkdirp(high_path)

    with open(os.path.join(low_path, 'repos.yaml'), 'w') as f:
        f.write('''\
repos:
- repo3
''')

    with open(os.path.join(high_path, 'repos.yaml'), 'w') as f:
        f.write('''\
repos:
- repo1
- repo2
''')

    assert config('get', 'repos').strip() == '''repos:
- repo1
- repo2
- repo3'''


def test_config_edit(mutable_config):
    """Ensure `spack config edit` edits the right paths."""
    user_path = spack.config.config.scopes['user'].path

    repos_path = os.path.join(user_path, 'repos.yaml')

    assert config('edit', '--print-file', 'repos').strip() == repos_path

    platform = spack.config.substitute_config_variables('$platform')
    platform_path = os.path.join(user_path, platform)
    mutable_config.push_scope(
        spack.config.ConfigScope('user/' + platform, platform_path))
    os.makedirs(platform_path)

    compilers_platform_path = os.path.join(platform_path, 'compilers.yaml')
    # Always return the platform-specific path for compilers regardless of
    # whether the file exists
    assert config('edit', '--print-file', 'compilers').strip() == (
        compilers_platform_path)

    repos_platform_path = os.path.join(platform_path, 'repos.yaml')
    with open(repos_platform_path, 'w') as config_file:
        config_file.write("""repos: []
""")
    # Now that a platform-specific repo config exists, that should be returned
    assert config('edit', '--print-file', 'repos').strip() == (
        repos_platform_path)


def test_config_get_gets_spack_yaml(mutable_mock_env_path):
    env = ev.create('test')

    config('get', fail_on_error=False)
    assert config.returncode == 1

    with env:
        config('get', fail_on_error=False)
        assert config.returncode == 1

        env.write()

        assert 'mpileaks' not in config('get')

        env.add('mpileaks')
        env.write()

        assert 'mpileaks' in config('get')


def test_config_edit_edits_spack_yaml(mutable_mock_env_path):
    env = ev.create('test')
    with env:
        assert config('edit', '--print-file').strip() == env.manifest_path


def test_config_edit_fails_correctly_with_no_env(mutable_mock_env_path):
    output = config('edit', '--print-file', fail_on_error=False)
    assert "requires a section argument or an active environment" in output


def test_config_get_fails_correctly_with_no_env(mutable_mock_env_path):
    output = config('get', fail_on_error=False)
    assert "requires a section argument or an active environment" in output
