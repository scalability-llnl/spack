# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from llnl.util.filesystem import mkdirp

import spack.config
import spack.environment as ev
from spack.main import SpackCommand

config = SpackCommand('config')
env = SpackCommand('env')

def test_get_config_scope(mock_low_high_config):
    assert config('get', 'compilers').strip() == 'compilers: {}'


def test_get_config_scope_merged(mock_low_high_config):
    low_path = mock_low_high_config.scopes['low'].path
    high_path = mock_low_high_config.scopes['high'].path

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


def test_config_edit():
    """Ensure `spack config edit` edits the right paths."""
    dms = spack.config.default_modify_scope()
    dms_path = spack.config.config.scopes[dms].path
    user_path = spack.config.config.scopes['user'].path

    comp_path = os.path.join(dms_path, 'compilers.yaml')
    repos_path = os.path.join(user_path, 'repos.yaml')

    assert config('edit', '--print-file', 'compilers').strip() == comp_path
    assert config('edit', '--print-file', 'repos').strip() == repos_path


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


def test_config_list():
    output = config('list')
    assert 'compilers' in output
    assert 'packages' in output


def test_config_add(mock_config):
    config('add', 'config:dirty:true')
    output = config('get', 'config')

    assert output == """config:
  dirty: true
"""


def test_config_add_list(mock_config):
    config('add', 'config:template_dirs:test1')
    config('add', 'config:template_dirs:[test2]')
    config('add', 'config:template_dirs:test3')
    output = config('get', 'config')

    assert output == """config:
  template_dirs:
  - test1
  - test2
  - test3
"""


def test_config_add_update_dict(mock_config):
    config('add', 'packages:all:compiler:[gcc]')  # TODO
    config('add', 'packages:all:version:1.0.0')
    output = config('get', 'packages')

    assert output == """packages:
  all:
    version:
    - 1.0.0
    compiler:
    - gcc
"""


def test_config_remove_value(mock_config):
    config('add', 'config:dirty:true')
    config('remove', 'config:dirty:true')
    output = config('get', 'config')

    assert output == """config: {}
"""


def test_config_remove_alias_rm(mock_config):
    config('add', 'config:dirty:true')
    config('rm', 'config:dirty:true')
    output = config('get', 'config')

    assert output == """config: {}
"""


def test_config_remove_dict(mock_config):
    config('add', 'config:dirty:true')
    config('rm', 'config:dirty')
    output = config('get', 'config')

    assert output == """config: {}
"""


def test_remove_from_list(mock_config):
    config('add', 'config:template_dirs:test1')
    config('add', 'config:template_dirs:[test2]')
    config('add', 'config:template_dirs:test3')
    config('remove', 'config:template_dirs:test2')
    output = config('get', 'config')

    assert output == """config:
  template_dirs:
  - test1
  - test3
"""


def test_remove_list(mock_config):
    config('add', 'config:template_dirs:test1')
    config('add', 'config:template_dirs:[test2]')
    config('add', 'config:template_dirs:test3')
    config('remove', 'config:template_dirs:[test2]')
    output = config('get', 'config')

    assert output == """config:
  template_dirs:
  - test1
  - test3
"""


def test_config_add_to_env(mock_config, mutable_mock_env_path):
    env = ev.create('test')
    with env:
        config('add', 'config:dirty:true')
        output = config('get')

    expected = ev.default_manifest_yaml
    expected += """  config:
    dirty: true

"""
    assert output == expected


def test_config_remove_from_env(mock_config, mutable_mock_env_path):
    env('create', 'test')

    with ev.read('test'):
        config('add', 'config:dirty:true')

    with ev.read('test'):
        config('rm', 'config:dirty')
        output = config('get')

    expected = ev.default_manifest_yaml
    expected += """  config: {}

"""
    assert output == expected
