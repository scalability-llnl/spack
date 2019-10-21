# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from llnl.util.filesystem import mkdirp

import spack.config
from spack.config import ConfigScope
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


def test_get_config_user_path_priority(mock_config, tmpdir):
    # the user_path config.yaml variable should
    # obey the usual scope priority hierarchy
    # when overriding the ~/.spack default

    # set up mock scope paths as usual
    low_path = mock_config.scopes['low'].path
    high_path = mock_config.scopes['high'].path
    mkdirp(low_path)
    mkdirp(high_path)

    # create two separate subdirectories where the user_path
    # will be assigned depending on scope priority
    user_low_path = os.path.join(str(tmpdir), 'low')
    user_high_path = os.path.join(str(tmpdir), 'high')

    for path in [user_low_path, user_high_path]:
        mkdirp(path)

    # we're going to remove and then restore the 'low' and
    # 'high' priority mock_config scopes, so that they
    # can gain priority when pushed back in---ideally we'd
    # test the built-in hierarchy directly, but we don't want
    # to i.e., modify local spack settings

    high_scope = mock_config.pop_scope()
    low_scope = mock_config.pop_scope()

    # make sure no scopes are currently available
    assert not mock_config.file_scopes

    # the default user_path remains ~/.spack
    # so loading in the default as the first scope
    # should return that value
    mock_config.push_scope(ConfigScope('defaults',
                           os.path.join(spack.paths.etc_path,
                                        'spack', 'defaults')))

    expected_path = "~/.spack"
    assert spack.config.get('config:user_path') == expected_path

    # the next added scope, "low", should override user_path with
    # its unique value for that setting

    with open(os.path.join(low_path, 'config.yaml'), 'w') as f:
        f.write('''\
config:
  user_path: {user_low_path}
'''.format(user_low_path=user_low_path))

    mock_config.push_scope(low_scope)
    assert spack.config.get('config:user_path') == user_low_path

    # check that if we set something with spack, it
    # starts populating user_low_path with files, consistent
    # with default ~/.spack behavior for the user_path

    # initially there should be only 1 file in the new user_path:
    files_present = os.listdir(user_low_path)
    assert len(files_present) == 1
    assert 'config.yaml' in files_present

    # if we add a repo, even one that doesn't really exist,
    # this should generate a file in the user path
    spack.config.set('repos',
                     [str(tmpdir)],
                     scope='low')

    files_present = os.listdir(user_low_path)
    assert len(files_present) == 2
    assert 'repos.yaml' in files_present

    # a high priority scope config.yaml addition to user_path
    # should override the lower priority value set above:

    with open(os.path.join(high_path, 'config.yaml'), 'w') as f:
        f.write('''\
config:
  user_path: {user_high_path}
'''.format(user_high_path=user_high_path))

    mock_config.push_scope(high_scope)
    assert spack.config.get('config:user_path') == user_high_path

    # confirm population of new user path once again,
    # this time looking for a mirrors.yaml file

    spack.config.set('mirrors',
                     {'dummy': str(tmpdir)})

    files_present = os.listdir(user_high_path)
    assert len(files_present) == 2
    assert 'mirrors.yaml' in files_present
    assert 'repos.yaml' not in files_present

    # make sure previous user_path is no longer being
    # "polluted"
    assert 'mirrors.yaml' not in os.listdir(user_low_path)


def test_misc_cache_user_path(tmpdir):
    # the misc_cache path should become rooted
    # in the user_path when user_path is set
    # by user to a non-default value, otherwise
    # we'd continue writing to ~/.spack/cache
    # when user_path is not ~/.spack

    # to avoid disrupting local spack instance,
    # create a duplicate configuration here with
    # a high priority scope pointing to a tmpdir path
    # added in

    from spack.config import configuration_paths, _config
    import llnl.util.lang

    test_config_path = os.path.join(str(tmpdir), 'test')
    mkdirp(test_config_path)
    new_config_path = ('test', test_config_path)

    with open(os.path.join(test_config_path, 'config.yaml'), 'w') as f:
        f.write('''\
config:
  user_path: {test_path}
'''.format(test_path=test_config_path))

    configuration_paths = list(configuration_paths)
    configuration_paths.append(new_config_path)

    spack.config.configuration_paths = tuple(configuration_paths)

    # flush through code path in the library by creating
    # the new singleton instance:
    test_config = llnl.util.lang.Singleton(_config)

    config = test_config.get('config')
    expected_misc_cache_path = os.path.join(test_config_path, 'cache')
    assert config['misc_cache'] == expected_misc_cache_path
