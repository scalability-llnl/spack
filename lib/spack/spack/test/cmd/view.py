# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.main import SpackCommand
import os.path
import pytest

import spack.util.spack_yaml as s_yaml

activate = SpackCommand('activate')
extensions = SpackCommand('extensions')
install = SpackCommand('install')
view = SpackCommand('view')


def create_projection_file(tmpdir, projection):
    if 'projections' not in projection:
        projection = {'projections': projection}

    projection_file = tmpdir.mkdir('projection').join('projection.yaml')
    projection_file.write(s_yaml.dump(projection))
    return projection_file


@pytest.mark.parametrize('cmd', ['hardlink', 'symlink', 'hard', 'add',
                                 'copy', 'relocate'])
def test_view_link_status(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery, cmd):
    install('libdwarf')
    viewpath = str(tmpdir.mkdir('view_{0}'.format(cmd)))
    view(cmd, viewpath, 'libdwarf')
    package_prefix = os.path.join(viewpath, 'libdwarf')
    assert os.path.exists(package_prefix)

    output = view('statlink', viewpath, 'libdwarf')
    assert 'Packages linked in [{0}]'.format(viewpath) in output


@pytest.mark.parametrize('cmd', ['hardlink', 'symlink', 'hard', 'add',
                                 'copy', 'relocate'])
def test_view_link_type(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery, cmd):
    install('libdwarf')
    viewpath = str(tmpdir.mkdir('view_{0}'.format(cmd)))
    view(cmd, viewpath, 'libdwarf')
    package_prefix = os.path.join(viewpath, 'libdwarf')
    assert os.path.exists(package_prefix)

    # Check that we use symlinks for and only for the appropriate subcommands
    is_link_cmd = cmd in ('symlink', 'add')
    assert os.path.islink(package_prefix) == is_link_cmd


@pytest.mark.parametrize('add_cmd', ['hardlink', 'symlink', 'hard', 'add',
                                     'copy', 'relocate'])
def test_view_link_type_remove(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery, add_cmd):
    install('needs-relocation')
    viewpath = str(tmpdir.mkdir('view_{0}'.format(add_cmd)))
    view(add_cmd, viewpath, 'needs-relocation')
    bindir = os.path.join(viewpath, 'bin')
    assert os.path.exists(bindir)

    view('remove', viewpath, 'needs-relocation')
    assert not os.path.exists(bindir)


@pytest.mark.parametrize('cmd', ['hardlink', 'symlink', 'hard', 'add',
                                 'copy', 'relocate'])
def test_view_projections(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery, cmd):
    install('libdwarf@20130207')

    viewpath = str(tmpdir.mkdir('view_{0}'.format(cmd)))
    view_projection = {
        'projections': {
            'all': '{name}-{version}'
        }
    }
    projection_file = create_projection_file(tmpdir, view_projection)
    view(cmd, viewpath, '--projection-file={0}'.format(projection_file),
         'libdwarf')

    package_prefix = os.path.join(viewpath, 'libdwarf-20130207/libdwarf')
    assert os.path.exists(package_prefix)

    # Check that we use symlinks for and only for the appropriate subcommands
    is_symlink_cmd = cmd in ('symlink', 'add')
    assert os.path.islink(package_prefix) == is_symlink_cmd


def test_view_multiple_projections(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('libdwarf@20130207')
    install('extendee@1.0%gcc')

    viewpath = str(tmpdir.mkdir('view'))
    view_projection = s_yaml.syaml_dict(
        [('extendee', '{name}-{compiler.name}'),
         ('all', '{name}-{version}')]
    )

    projection_file = create_projection_file(tmpdir, view_projection)
    view('add', viewpath, '--projection-file={0}'.format(projection_file),
         'libdwarf', 'extendee')

    libdwarf_prefix = os.path.join(viewpath, 'libdwarf-20130207/libdwarf')
    extendee_prefix = os.path.join(viewpath, 'extendee-gcc/bin')
    assert os.path.exists(libdwarf_prefix)
    assert os.path.exists(extendee_prefix)


def test_view_multiple_projections_all_first(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('libdwarf@20130207')
    install('extendee@1.0%gcc')

    viewpath = str(tmpdir.mkdir('view'))
    view_projection = s_yaml.syaml_dict(
        [('all', '{name}-{version}'),
         ('extendee', '{name}-{compiler.name}')]
    )

    projection_file = create_projection_file(tmpdir, view_projection)
    view('add', viewpath, '--projection-file={0}'.format(projection_file),
         'libdwarf', 'extendee')

    libdwarf_prefix = os.path.join(viewpath, 'libdwarf-20130207/libdwarf')
    extendee_prefix = os.path.join(viewpath, 'extendee-gcc/bin')
    assert os.path.exists(libdwarf_prefix)
    assert os.path.exists(extendee_prefix)


def test_view_external(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('externaltool')
    viewpath = str(tmpdir.mkdir('view'))
    output = view('symlink', viewpath, 'externaltool')
    assert 'Skipping external package: externaltool' in output


def test_view_extension(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    install('extension2@1.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    all_installed = extensions('--show', 'installed', 'extendee')
    assert 'extension1@1.0' in all_installed
    assert 'extension1@2.0' in all_installed
    assert 'extension2@1.0' in all_installed
    global_activated = extensions('--show', 'activated', 'extendee')
    assert 'extension1@1.0' not in global_activated
    assert 'extension1@2.0' not in global_activated
    assert 'extension2@1.0' not in global_activated
    view_activated = extensions('--show', 'activated',
                                '-v', viewpath,
                                'extendee')
    assert 'extension1@1.0' in view_activated
    assert 'extension1@2.0' not in view_activated
    assert 'extension2@1.0' not in view_activated
    assert os.path.exists(os.path.join(viewpath, 'bin', 'extension1'))


def test_view_extension_projection(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee@1.0')
    install('extension1@1.0')
    install('extension1@2.0')
    install('extension2@1.0')

    viewpath = str(tmpdir.mkdir('view'))
    view_projection = {'all': '{name}-{version}'}
    projection_file = create_projection_file(tmpdir, view_projection)
    view('symlink', viewpath, '--projection-file={0}'.format(projection_file),
         'extension1@1.0')

    all_installed = extensions('--show', 'installed', 'extendee')
    assert 'extension1@1.0' in all_installed
    assert 'extension1@2.0' in all_installed
    assert 'extension2@1.0' in all_installed
    global_activated = extensions('--show', 'activated', 'extendee')
    assert 'extension1@1.0' not in global_activated
    assert 'extension1@2.0' not in global_activated
    assert 'extension2@1.0' not in global_activated
    view_activated = extensions('--show', 'activated',
                                '-v', viewpath,
                                'extendee')
    assert 'extension1@1.0' in view_activated
    assert 'extension1@2.0' not in view_activated
    assert 'extension2@1.0' not in view_activated

    assert os.path.exists(os.path.join(viewpath, 'extendee-1.0',
                                       'bin', 'extension1'))


def test_view_extension_remove(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    view('remove', viewpath, 'extension1@1.0')
    all_installed = extensions('--show', 'installed', 'extendee')
    assert 'extension1@1.0' in all_installed
    global_activated = extensions('--show', 'activated', 'extendee')
    assert 'extension1@1.0' not in global_activated
    view_activated = extensions('--show', 'activated',
                                '-v', viewpath,
                                'extendee')
    assert 'extension1@1.0' not in view_activated
    assert not os.path.exists(os.path.join(viewpath, 'bin', 'extension1'))


def test_view_extension_conflict(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    output = view('symlink', viewpath, 'extension1@2.0')
    assert 'Package conflict detected' in output


def test_view_extension_conflict_ignored(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    view('symlink', viewpath, '-i', 'extension1@2.0')
    with open(os.path.join(viewpath, 'bin', 'extension1'), 'r') as fin:
        assert fin.read() == '1.0'


def test_view_extension_global_activation(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    install('extension2@1.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    activate('extension1@2.0')
    activate('extension2@1.0')
    all_installed = extensions('--show', 'installed', 'extendee')
    assert 'extension1@1.0' in all_installed
    assert 'extension1@2.0' in all_installed
    assert 'extension2@1.0' in all_installed
    global_activated = extensions('--show', 'activated', 'extendee')
    assert 'extension1@1.0' not in global_activated
    assert 'extension1@2.0' in global_activated
    assert 'extension2@1.0' in global_activated
    view_activated = extensions('--show', 'activated',
                                '-v', viewpath,
                                'extendee')
    assert 'extension1@1.0' in view_activated
    assert 'extension1@2.0' not in view_activated
    assert 'extension2@1.0' not in view_activated
    assert os.path.exists(os.path.join(viewpath, 'bin', 'extension1'))
    assert not os.path.exists(os.path.join(viewpath, 'bin', 'extension2'))


def test_view_extendee_with_global_activations(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    install('extension2@1.0')
    viewpath = str(tmpdir.mkdir('view'))
    activate('extension1@2.0')
    output = view('symlink', viewpath, 'extension1@1.0')
    assert 'Error: Globally activated extensions cannot be used' in output


def test_view_fails_with_missing_projections_file(tmpdir):
    viewpath = str(tmpdir.mkdir('view'))
    projection_file = os.path.join(str(tmpdir), 'nonexistent')
    with pytest.raises(SystemExit):
        view('symlink', '--projection-file', projection_file, viewpath, 'foo')
