# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest
import spack.config
import spack.environment
from spack.main import SpackCommand, SpackCommandError

banned_commands = [
    ('edit',),
    ('create',),
    ('test-env',),
    ('build-env',),
    ('ci', 'generate'),  # requires subcommand to parse
    ('dev-build',),
    ('config', 'add'),
    ('config', 'remove', 'foo'),  # requires argument to parse
    ('config', 'edit'),
    ('config', 'update', 'repos'),  # requires section to parse
    ('config', 'revert', 'repos'),
    ('external', 'find'),
    ('mirror', 'add', 'foo', 'bar'),
    ('mirror', 'remove', 'foo'),
    ('mirror', 'rm', 'foo'),
    ('repo', 'add', 'foo'),
    ('repo', 'remove', 'foo'),
    ('repo', 'rm', 'foo'),
    ('tutorial',),
    ('python',),
    ('develop',),
    ('undevelop',),
    ('compiler', 'find'),
    ('compiler', 'add'),
    ('compiler', 'remove', 'foo'),
    ('compiler', 'rm', 'foo'),
    ('env', 'activate', 'foo'),
    ('env', 'deactivate'),
    ('env', 'remove', 'foo'),
    ('env', 'view', 'enable'),
    ('env', 'view', 'disable'),
    ('env', 'update', 'foo'),
    ('env', 'revert', 'foo'),
    ('buildcache', 'install'),
    ('buildcache', 'keys'),
    ('gpg', 'create', 'foo', 'bar'),
    ('gpg', 'init'),
    ('gpg', 'trust', 'foo'),
    ('gpg', 'untrust', 'foo'),
    ('gpg', 'export', 'foo'),
]


@pytest.fixture
def deployment_mode(mutable_mock_env_path, monkeypatch):
    env_cmd = SpackCommand('env')
    env_cmd('create', 'test')

    monkeypatch.setattr(spack.environment, '_active_environment',
                        spack.environment.read('test'))

    def return_deployment_mode(*args, **kwargs):
        return {'deployment': {'env': 'test'}}
    monkeypatch.setattr(spack.config.restricted_config, 'get',
                        return_deployment_mode)
    yield


def test_banned_commands_fail_deployment_mode(deployment_mode):
    for command in banned_commands:
        with pytest.raises(SpackCommandError):
            SpackCommand(command[0])(*(command[1:]))


def test_modified_install_args_deployment_mode(deployment_mode):
    # The --cache-only option that is set by deployment mode is first to cause
    # an error in the test environment, so we test for that error message.
    install = SpackCommand('install')
    output = install('libelf', fail_on_error=False)
    assert 'found when cache-only' in output
    assert 'Error: No binary' in output
