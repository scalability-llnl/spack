# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import os
import os.path

import pytest

import spack
import spack.detection.path
import spack.util.spack_yaml as syaml
from spack.spec import Spec
from spack.main import SpackCommand


def test_find_external_single_package(mock_executable):
    pkgs_to_check = [spack.repo.get('cmake')]

    cmake_path = mock_executable("cmake", output='echo "cmake version 1.foo"')
    system_path_to_exe = {cmake_path: 'cmake'}

    pkg_to_entries = spack.detection.path.detect(
        pkgs_to_check, system_path_to_exe)

    pkg, entries = next(iter(pkg_to_entries.items()))
    single_entry = next(iter(entries))

    assert single_entry == Spec('cmake@1.foo')


def test_find_external_two_instances_same_package(mock_executable):
    pkgs_to_check = [spack.repo.get('cmake')]

    # Each of these cmake instances is created in a different prefix
    cmake_path1 = mock_executable(
        "cmake", output='echo "cmake version 1.foo"', subdir=('base1', 'bin')
    )
    cmake_path2 = mock_executable(
        "cmake", output='echo "cmake version 3.17.2"', subdir=('base2', 'bin')
    )
    system_path_to_exe = {
        cmake_path1: 'cmake',
        cmake_path2: 'cmake'}

    pkg_to_entries = spack.detection.path.detect(
        pkgs_to_check, system_path_to_exe
    )

    pkg, external_specs = next(iter(pkg_to_entries.items()))
    spec_to_path = dict((s, s.external_path) for s in external_specs)
    assert spec_to_path[Spec('cmake@1.foo')] == (
        spack.detection.path._determine_base_dir(os.path.dirname(cmake_path1)))
    assert spec_to_path[Spec('cmake@3.17.2')] == (
        spack.detection.path._determine_base_dir(os.path.dirname(cmake_path2)))


def test_find_external_update_config(mutable_config):
    entries = [
        Spec.from_detection('cmake@1.foo', external_path='/x/y1/'),
        Spec.from_detection('cmake@3.17.2', external_path='/x/y2/'),
    ]
    pkg_to_entries = {'cmake': entries}

    spack.cmd.external._update_pkg_config(pkg_to_entries, False)

    pkgs_cfg = spack.config.get('packages')
    cmake_cfg = pkgs_cfg['cmake']
    cmake_externals = cmake_cfg['externals']

    assert {'spec': 'cmake@1.foo', 'prefix': '/x/y1/'} in cmake_externals
    assert {'spec': 'cmake@3.17.2', 'prefix': '/x/y2/'} in cmake_externals


def test_get_executables(working_env, mock_executable):
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")

    os.environ['PATH'] = ':'.join([os.path.dirname(cmake_path1)])
    path_to_exe = spack.detection.path.system_executables()
    assert path_to_exe[cmake_path1] == 'cmake'


external = SpackCommand('external')


def test_find_external_cmd(mutable_config, working_env, mock_executable):
    """Test invoking 'spack external find' with additional package arguments,
    which restricts the set of packages that Spack looks for.
    """
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    prefix = os.path.dirname(os.path.dirname(cmake_path1))

    os.environ['PATH'] = ':'.join([os.path.dirname(cmake_path1)])
    external('find', 'cmake')

    pkgs_cfg = spack.config.get('packages')
    cmake_cfg = pkgs_cfg['cmake']
    cmake_externals = cmake_cfg['externals']

    assert {'spec': 'cmake@1.foo', 'prefix': prefix} in cmake_externals


def test_find_external_cmd_not_buildable(
        mutable_config, working_env, mock_executable):
    """When the user invokes 'spack external find --not-buildable', the config
    for any package where Spack finds an external version should be marked as
    not buildable.
    """
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    os.environ['PATH'] = ':'.join([os.path.dirname(cmake_path1)])
    external('find', '--not-buildable', 'cmake')
    pkgs_cfg = spack.config.get('packages')
    assert not pkgs_cfg['cmake']['buildable']


def test_find_external_cmd_full_repo(
        mutable_config, working_env, mock_executable, mutable_mock_repo):
    """Test invoking 'spack external find' with no additional arguments, which
    iterates through each package in the repository.
    """

    exe_path1 = mock_executable(
        "find-externals1-exe", output="echo find-externals1 version 1.foo"
    )
    prefix = os.path.dirname(os.path.dirname(exe_path1))

    os.environ['PATH'] = ':'.join([os.path.dirname(exe_path1)])
    external('find')

    pkgs_cfg = spack.config.get('packages')
    pkg_cfg = pkgs_cfg['find-externals1']
    pkg_externals = pkg_cfg['externals']

    assert {'spec': 'find-externals1@1.foo', 'prefix': prefix} in pkg_externals


def test_find_external_merge(mutable_config, mutable_mock_repo):
    """Check that 'spack find external' doesn't overwrite an existing spec
    entry in packages.yaml.
    """
    pkgs_cfg_init = {
        'find-externals1': {
            'externals': [{
                'spec': 'find-externals1@1.1',
                'prefix': '/preexisting-prefix/'
            }],
            'buildable': False
        }
    }

    mutable_config.update_config('packages', pkgs_cfg_init)
    entries = [
        Spec.from_detection('find-externals1@1.1', external_path='/x/y1/'),
        Spec.from_detection('find-externals1@1.2', external_path='/x/y2/')
    ]
    pkg_to_entries = {'find-externals1': entries}
    spack.cmd.external._update_pkg_config(pkg_to_entries, False)

    pkgs_cfg = spack.config.get('packages')
    pkg_cfg = pkgs_cfg['find-externals1']
    pkg_externals = pkg_cfg['externals']

    assert {'spec': 'find-externals1@1.1',
            'prefix': '/preexisting-prefix/'} in pkg_externals
    assert {'spec': 'find-externals1@1.2',
            'prefix': '/x/y2/'} in pkg_externals


def test_list_detectable_packages(mutable_config, mutable_mock_repo):
    external("list")
    assert external.returncode == 0


def test_packages_yaml_format(mock_executable, mutable_config, monkeypatch):
    # Prepare an environment to detect a fake gcc
    gcc_exe = mock_executable('gcc', output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv('PATH', prefix)

    # Find the external spec
    external('find', 'gcc')

    # Check entries in 'packages.yaml'
    packages_yaml = spack.config.get('packages')
    assert 'gcc' in packages_yaml
    assert 'externals' in packages_yaml['gcc']
    externals = packages_yaml['gcc']['externals']
    assert len(externals) == 1
    external_gcc = externals[0]
    assert external_gcc['spec'] == 'gcc@4.2.1 languages=c'
    assert external_gcc['prefix'] == os.path.dirname(prefix)
    assert 'extra_attributes' in external_gcc
    extra_attributes = external_gcc['extra_attributes']
    assert 'prefix' not in extra_attributes
    assert extra_attributes['compilers']['c'] == gcc_exe


def test_overriding_prefix(mock_executable, mutable_config, monkeypatch):
    # Prepare an environment to detect a fake gcc that
    # override its external prefix
    gcc_exe = mock_executable('gcc', output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv('PATH', prefix)

    @classmethod
    def _determine_variants(cls, exes, version_str):
        return 'languages=c', {
            'prefix': '/opt/gcc/bin',
            'compilers': {'c': exes[0]}
        }

    gcc_cls = spack.repo.path.get_pkg_class('gcc')
    monkeypatch.setattr(gcc_cls, 'determine_variants', _determine_variants)

    # Find the external spec
    external('find', 'gcc')

    # Check entries in 'packages.yaml'
    packages_yaml = spack.config.get('packages')
    assert 'gcc' in packages_yaml
    assert 'externals' in packages_yaml['gcc']
    externals = packages_yaml['gcc']['externals']
    assert len(externals) == 1
    assert externals[0]['prefix'] == '/opt/gcc/bin'


def test_new_entries_are_reported_correctly(
        mock_executable, mutable_config, monkeypatch
):
    # Prepare an environment to detect a fake gcc
    gcc_exe = mock_executable('gcc', output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv('PATH', prefix)

    # The first run will find and add the external gcc
    output = external('find', 'gcc')
    assert 'The following specs have been' in output

    # The second run should report that no new external
    # has been found
    output = external('find', 'gcc')
    assert 'No new external packages detected' in output


def candidate_packages():
    all_packages = spack.repo.path.all_packages()
    to_be_tested = []
    for pkg in all_packages:
        pkg_dir = os.path.dirname(
            spack.repo.path.filename_for_package_name(pkg.name)
        )
        detection_data = os.path.join(pkg_dir, 'detection_test.yaml')
        if os.path.exists(detection_data):
            to_be_tested.append(pkg.name)
    return to_be_tested


@pytest.mark.detection
@pytest.mark.parametrize('package_name', candidate_packages())
def test_package_detection(mock_executable, package_name):
    def detection_tests_for(pkg):
        pkg_dir = os.path.dirname(
            spack.repo.path.filename_for_package_name(pkg)
        )
        detection_data = os.path.join(pkg_dir, 'detection_test.yaml')
        with open(detection_data) as f:
            return syaml.load(f)

    @contextlib.contextmanager
    def setup_test_layout(layout):
        exes_by_path, to_be_removed = {}, []
        for binary in layout:
            exe = mock_executable(
                binary['name'], binary['output'], subdir=binary['subdir']
            )
            to_be_removed.append(exe)
            exes_by_path[str(exe)] = os.path.basename(str(exe))

        yield exes_by_path

        for exe in to_be_removed:
            os.unlink(exe)

    # Retrieve detection test data for this package and cycle over each
    # of the scenarios that are encoded
    detection_tests = detection_tests_for(package_name)
    if 'paths' not in detection_tests:
        msg = 'Package "{0}" has no detection tests based on PATH'
        pytest.skip(msg.format(package_name))

    for test in detection_tests['paths']:
        # Setup the mock layout for detection. The context manager will
        # remove mock files when it's finished.
        with setup_test_layout(test['layout']) as abs_path_to_exe:
            entries = spack.detection.path.detect(
                [spack.repo.get(package_name)], abs_path_to_exe
            )
            specs = set(entries[package_name])
            results = test['results']
            # If no result was expected, check that nothing was detected
            if not results:
                msg = 'No spec was expected [detected={0}]'
                assert not specs, msg.format(sorted(specs))
                continue

            # If we expected results check that all of the expected
            # specs were detected.
            for result in results:
                spec, msg = result['spec'], 'Not able to detect "{0}"'
                assert spack.spec.Spec(spec) in specs, msg.format(str(spec))


@pytest.mark.detection
@pytest.mark.parametrize('package_name', candidate_packages())
def test_package_detection_on_cray(monkeypatch, mock_executable, package_name):
    import spack.architecture
    import spack.platforms.test
    import spack.detection.craype
    import spack.util.executable
    import spack.util.module_cmd
    import functools

    monkeypatch.setattr(spack.platforms.test.Test, 'front_os', 'sles15')
    monkeypatch.setattr(spack.platforms.test.Test, 'back_os', 'cnl7')
    monkeypatch.setattr(spack.platforms.test.Test, 'default_os', 'cnl7')
    monkeypatch.setattr(spack.architecture, 'platform',
                        lambda: spack.platforms.test.Test())

    # TODO: factor common code with previous test
    def detection_tests_for(pkg):
        pkg_dir = os.path.dirname(
            spack.repo.path.filename_for_package_name(pkg)
        )
        detection_data = os.path.join(pkg_dir, 'detection_test.yaml')
        with open(detection_data) as f:
            return syaml.load(f)

    @contextlib.contextmanager
    def setup_module_command(module_info):
        # Monkey-patch the module function to return mock output
        module = mock_executable('module', module_info['output'])
        orig_module_cmd = spack.util.module_cmd.module
        module_cmd = spack.util.executable.Executable(module)
        spack.util.module_cmd.module = functools.partial(
            module_cmd, output=str, error=str
        )

        yield

        spack.util.module_cmd.module = orig_module_cmd
        os.unlink(str(module))

    # Retrieve detection test data for this package and cycle over each
    # of the scenarios that are encoded
    detection_tests = detection_tests_for(package_name)
    if 'craype' not in detection_tests:
        pytest.skip(
            'Package "{0}" has no detection test for Cray'.format(package_name)
        )

    for test in detection_tests['craype']:
        # Setup the mock layout for detection. The context manager will
        # remove mock files when it's finished.
        with setup_module_command(test['module']):
            entries = spack.detection.craype._detect_from_craype_modules(
                [spack.repo.get(package_name)]
            )
            # TODO: this part of the test is the same as above
            specs = set(entries[package_name])
            results = test['results']
            # If no result was expected, check that nothing was detected
            if not results:
                msg = 'No spec was expected [detected={0}]'
                assert not specs, msg.format(sorted(specs))
                continue

            # If we expected results check that all of the expected
            # specs were detected.
            for result in results:
                spec, msg = result['spec'], 'Not able to detect "{0}"'
                assert spack.spec.Spec(spec) in specs, msg.format(str(spec))
