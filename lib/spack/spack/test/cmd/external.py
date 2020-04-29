# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os
import stat

import spack
from spack.spec import Spec
from spack.cmd.external import ExternalPackageEntry
from spack.main import SpackCommand


@pytest.fixture()
def create_exe(tmpdir_factory):
    def _create_exe(exe_name, content):
        base_prefix = tmpdir_factory.mktemp('base-prefix')
        base_prefix.ensure('bin', dir=True)
        exe_path = str(base_prefix.join('bin', exe_name))
        with open(exe_path, 'w') as f:
            f.write("""\
#!/bin/bash

echo "{0}"
""".format(content))

        st = os.stat(exe_path)
        os.chmod(exe_path, st.st_mode | stat.S_IEXEC)
        return exe_path

    yield _create_exe


def test_find_external_single_package(create_exe):
    pkgs_to_check = [spack.repo.get('cmake')]

    cmake_path = create_exe("cmake", "cmake version 1.foo")
    system_path_to_exe = {cmake_path: 'cmake'}

    pkg_to_entries = spack.cmd.external._get_external_packages(
        pkgs_to_check, system_path_to_exe)

    pkg, entries = next(iter(pkg_to_entries.items()))
    single_entry = next(iter(entries))

    assert single_entry.spec == Spec('cmake@1.foo')


def test_find_external_two_instances_same_package(create_exe):
    pkgs_to_check = [spack.repo.get('cmake')]

    cmake_path1 = create_exe("cmake", "cmake version 1.foo")
    cmake_path2 = create_exe("cmake", "cmake version 3.17.2")
    system_path_to_exe = {
        cmake_path1: 'cmake',
        cmake_path2: 'cmake'}

    pkg_to_entries = spack.cmd.external._get_external_packages(
        pkgs_to_check, system_path_to_exe)

    pkg, entries = next(iter(pkg_to_entries.items()))
    collected_specs = set(entry.spec for entry in entries)
    assert set([Spec('cmake@1.foo'), Spec('cmake@3.17.2')]) == collected_specs


def test_find_external_update_config(mutable_config):
    pkg_to_entries = {
        'cmake': [
            ExternalPackageEntry(Spec('cmake@1.foo'), '/x/y1/'),
            ExternalPackageEntry(Spec('cmake@3.17.2'), '/x/y2/'),
        ]
    }

    spack.cmd.external._update_pkg_config(pkg_to_entries)

    pkgs_cfg = spack.config.get('packages')
    cmake_cfg = pkgs_cfg['cmake']
    cmake_paths_cfg = cmake_cfg['paths']

    assert cmake_paths_cfg['cmake@1.foo'] == '/x/y1/'
    assert cmake_paths_cfg['cmake@3.17.2'] == '/x/y2/'


def test_get_executables(working_env, create_exe):
    cmake_path1 = create_exe("cmake", "cmake version 1.foo")

    os.environ['PATH'] = ':'.join([os.path.dirname(cmake_path1)])
    path_to_exe = spack.cmd.external._get_system_executables()
    assert path_to_exe[cmake_path1] == 'cmake'


external = SpackCommand('external')


def test_find_external_command(mutable_config, working_env, create_exe):
    """Test invoking 'spack external find' with additional package arguments,
    which restricts the set of packages that Spack looks for.
    """
    cmake_path1 = create_exe("cmake", "cmake version 1.foo")

    os.environ['PATH'] = ':'.join([os.path.dirname(cmake_path1)])
    external('find', 'cmake')

    pkgs_cfg = spack.config.get('packages')
    cmake_cfg = pkgs_cfg['cmake']
    cmake_paths_cfg = cmake_cfg['paths']

    assert 'cmake@1.foo' in cmake_paths_cfg


def test_find_external_command_full_repo(
    mutable_config, working_env, create_exe, mutable_mock_repo):
    """Test invoking 'spack external find' with no additional arguments, which
    iterates through each package in the repository.
    """

    exe_path1 = create_exe(
        "find-externals1-exe", "find-externals1 version 1.foo")

    os.environ['PATH'] = ':'.join([os.path.dirname(exe_path1)])
    external('find')

    pkgs_cfg = spack.config.get('packages')
    pkg_cfg = pkgs_cfg['find-externals1']
    pkg_paths_cfg = pkg_cfg['paths']

    assert 'find-externals1@1.foo' in pkg_paths_cfg


def test_find_external_merge(mutable_config, mutable_mock_repo):
    pkgs_cfg_init = {
        'find-externals1': {
            'paths': {
                'find-externals1@1.1': '/preexisting-prefix/'
            },
            'buildable': False
        }
    }

    mutable_config.update_config('packages', pkgs_cfg_init)

    pkg_to_entries = {
        'find-externals1': [
            ExternalPackageEntry(Spec('find-externals1@1.1'), '/x/y1/'),
            ExternalPackageEntry(Spec('find-externals1@1.2'), '/x/y2/'),
        ]
    }
    spack.cmd.external._update_pkg_config(pkg_to_entries)

    pkgs_cfg = spack.config.get('packages')
    pkg_cfg = pkgs_cfg['find-externals1']
    pkg_paths_cfg = pkg_cfg['paths']

    assert pkg_paths_cfg['find-externals1@1.1'] == '/preexisting-prefix/'
    assert pkg_paths_cfg['find-externals1@1.2'] == '/x/y2/'
