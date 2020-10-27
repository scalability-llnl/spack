# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os
import os.path

from spack.main import SpackCommand, SpackCommandError
import spack.environment as ev
import spack.config

mirror = SpackCommand('mirror')
env = SpackCommand('env')
add = SpackCommand('add')
concretize = SpackCommand('concretize')


@pytest.fixture
def tmp_scope():
    """Creates a temporary configuration scope"""

    base_name = 'internal-testing-scope'
    current_overrides = set(
        x.name for x in
        spack.config.config.matching_scopes(r'^{0}'.format(base_name)))

    num_overrides = 0
    scope_name = base_name
    while scope_name in current_overrides:
        scope_name = '{0}{1}'.format(base_name, num_overrides)
        num_overrides += 1

    with spack.config.override(spack.config.InternalConfigScope(scope_name)):
        yield scope_name


@pytest.mark.disable_clean_stage_check
@pytest.mark.regression('8083')
def test_regression_8083(tmpdir, capfd, mock_packages, mock_fetch, config):
    with capfd.disabled():
        output = mirror('create', '-d', str(tmpdir), 'externaltool')
    assert 'Skipping' in output
    assert 'as it is an external spec' in output


@pytest.mark.regression('17531')
def test_regression_17531(tmp_scope, tmpdir, capfd, mock_packages, mock_fetch, config):
    tmp_mirror0 = (
        'file://' + os.path.abspath(os.path.join(str(tmpdir), 'mirror-0')))

    tmp_mirror1 = (
        'file://' + os.path.abspath(os.path.join(str(tmpdir), 'mirror-1')))

    with capfd.disabled():
        output = mirror('create',
                        '--mirror-url',
                        tmp_mirror0,
                        '--skip-unstable-versions',
                        'git-test',
                        'trivial-pkg-with-valid-hash')

        assert ('Successfully created mirror in ' + tmp_mirror0) in output

        mirror('add', '--scope', 'command_line', 'named-mirror', tmp_mirror1)

        output = mirror('create',
                        '--mirror-name',
                        'named-mirror',
                        '--skip-unstable-versions',
                        'git-test',
                        'trivial-pkg-with-valid-hash')

        assert ('Successfully created mirror in ' + tmp_mirror1) in output

        mirror('remove', '--scope', 'command_line', 'named-mirror')


@pytest.mark.regression('12345')
def test_mirror_from_env(tmpdir, mock_packages, mock_fetch, config,
                         mutable_mock_env_path):
    mirror_dir = str(tmpdir)
    env_name = 'test'

    env('create', env_name)
    with ev.read(env_name):
        add('trivial-install-test-package')
        add('git-test')
        concretize()
        with spack.config.override('config:checksum', False):
            mirror('create', '-d', mirror_dir, '--all')

    e = ev.read(env_name)
    assert set(os.listdir(mirror_dir)) == set([s.name for s in e.user_specs])
    for spec in e.specs_by_hash.values():
        mirror_res = os.listdir(os.path.join(mirror_dir, spec.name))
        expected = ['%s.tar.gz' % spec.format('{name}-{version}')]
        assert mirror_res == expected


@pytest.fixture
def source_for_pkg_with_hash(mock_packages, tmpdir):
    pkg = spack.repo.get('trivial-pkg-with-valid-hash')
    local_url_basename = os.path.basename(pkg.url)
    local_path = os.path.join(str(tmpdir), local_url_basename)
    with open(local_path, 'w') as f:
        f.write(pkg.hashed_content)
    local_url = "file://" + local_path
    pkg.versions[spack.version.Version('1.0')]['url'] = local_url


def test_mirror_skip_unstable(tmpdir_factory, mock_packages, config,
                              source_for_pkg_with_hash):
    mirror_dir = str(tmpdir_factory.mktemp('mirror-dir'))

    specs = [spack.spec.Spec(x).concretized() for x in
             ['git-test', 'trivial-pkg-with-valid-hash']]
    spack.mirror.create(mirror_dir, specs, skip_unstable_versions=True)

    assert (set(os.listdir(mirror_dir)) - set(['_source-cache']) ==
            set(['trivial-pkg-with-valid-hash']))


class MockMirrorArgs(object):
    def __init__(self, specs=None, all=False, file=None,
                 versions_per_spec=None, dependencies=False,
                 exclude_file=None, exclude_specs=None):
        self.specs = specs or []
        self.all = all
        self.file = file
        self.versions_per_spec = versions_per_spec
        self.dependencies = dependencies
        self.exclude_file = exclude_file
        self.exclude_specs = exclude_specs


def test_exclude_specs(mock_packages):
    args = MockMirrorArgs(
        specs=['mpich'],
        versions_per_spec='all',
        exclude_specs="mpich@3.0.1:3.0.2 mpich@1.0")

    mirror_specs = spack.cmd.mirror._determine_specs_to_mirror(args)
    expected_include = set(spack.spec.Spec(x) for x in
                           ['mpich@3.0.3', 'mpich@3.0.4', 'mpich@3.0'])
    expected_exclude = set(spack.spec.Spec(x) for x in
                           ['mpich@3.0.1', 'mpich@3.0.2', 'mpich@1.0'])
    assert expected_include <= set(mirror_specs)
    assert (not expected_exclude & set(mirror_specs))


def test_exclude_file(mock_packages, tmpdir):
    exclude_path = os.path.join(str(tmpdir), 'test-exclude.txt')
    with open(exclude_path, 'w') as exclude_file:
        exclude_file.write("""\
mpich@3.0.1:3.0.2
mpich@1.0
""")

    args = MockMirrorArgs(
        specs=['mpich'],
        versions_per_spec='all',
        exclude_file=exclude_path)

    mirror_specs = spack.cmd.mirror._determine_specs_to_mirror(args)
    expected_include = set(spack.spec.Spec(x) for x in
                           ['mpich@3.0.3', 'mpich@3.0.4', 'mpich@3.0'])
    expected_exclude = set(spack.spec.Spec(x) for x in
                           ['mpich@3.0.1', 'mpich@3.0.2', 'mpich@1.0'])
    assert expected_include <= set(mirror_specs)
    assert (not expected_exclude & set(mirror_specs))


def test_mirror_crud(tmp_scope, capsys):
    with capsys.disabled():
        mirror('add', '--scope', tmp_scope, 'mirror', 'http://spack.io')

        output = mirror('remove', '--scope', tmp_scope, 'mirror')
        assert 'Removed mirror' in output

        mirror('add', '--scope', tmp_scope, 'mirror', 'http://spack.io')

        # no-op
        output = mirror('set-url', '--scope', tmp_scope,
                        'mirror', 'http://spack.io')
        assert 'Url already set' in output

        output = mirror('set-url', '--scope', tmp_scope,
                        '--push', 'mirror', 's3://spack-public')
        assert 'Changed (push) url' in output

        # no-op
        output = mirror('set-url', '--scope', tmp_scope,
                        '--push', 'mirror', 's3://spack-public')
        assert 'Url already set' in output

        output = mirror('remove', '--scope', tmp_scope, 'mirror')
        assert 'Removed mirror' in output

        output = mirror('list', '--scope', tmp_scope)
        assert 'No mirrors configured' in output


def test_mirror_nonexisting(tmp_scope):
    with pytest.raises(SpackCommandError):
        mirror('remove', '--scope', tmp_scope, 'not-a-mirror')

    with pytest.raises(SpackCommandError):
        mirror('set-url', '--scope', tmp_scope,
               'not-a-mirror', 'http://spack.io')


def test_mirror_name_collision(tmp_scope):
    mirror('add', '--scope', tmp_scope, 'first', '1')

    with pytest.raises(SpackCommandError):
        mirror('add', '--scope', tmp_scope, 'first', '1')
