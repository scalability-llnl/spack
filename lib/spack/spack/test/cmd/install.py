# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import filecmp
import os
import re
import shutil
import time

import pytest
from six.moves import builtins

import llnl.util.filesystem as fs

import spack.cmd.install
import spack.compilers as compilers
import spack.config
import spack.environment as ev
import spack.hash_types as ht
import spack.package
import spack.util.executable
from spack.error import SpackError
from spack.main import SpackCommand
from spack.spec import CompilerSpec, Spec

install = SpackCommand('install')
env = SpackCommand('env')
add = SpackCommand('add')
mirror = SpackCommand('mirror')
uninstall = SpackCommand('uninstall')
buildcache = SpackCommand('buildcache')
find = SpackCommand('find')


@pytest.fixture()
def noop_install(monkeypatch):
    def noop(*args, **kwargs):
        pass
    monkeypatch.setattr(spack.installer.PackageInstaller, 'install', noop)


def test_install_package_and_dependency(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):

    with tmpdir.as_cwd():
        install('--log-format=junit', '--log-file=test.xml', 'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content


@pytest.mark.disable_clean_stage_check
def test_install_runtests_notests(monkeypatch, mock_packages, install_mockery):
    def check(pkg):
        assert not pkg.run_tests
    monkeypatch.setattr(spack.package.PackageBase, 'unit_test_check', check)
    install('-v', 'dttop')


@pytest.mark.disable_clean_stage_check
def test_install_runtests_root(monkeypatch, mock_packages, install_mockery):
    def check(pkg):
        assert pkg.run_tests == (pkg.name == 'dttop')

    monkeypatch.setattr(spack.package.PackageBase, 'unit_test_check', check)
    install('--test=root', 'dttop')


@pytest.mark.disable_clean_stage_check
def test_install_runtests_all(monkeypatch, mock_packages, install_mockery):
    def check(pkg):
        assert pkg.run_tests

    monkeypatch.setattr(spack.package.PackageBase, 'unit_test_check', check)
    install('--test=all', 'a')
    install('--run-tests', 'a')


def test_install_package_already_installed(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):

    with tmpdir.as_cwd():
        install('libdwarf')
        install('--log-format=junit', '--log-file=test.xml', 'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content

    skipped = [line for line in content.split('\n') if 'skipped' in line]
    assert len(skipped) == 2


@pytest.mark.parametrize('arguments,expected', [
    ([], spack.config.get('config:dirty')),  # default from config file
    (['--clean'], False),
    (['--dirty'], True),
])
def test_install_dirty_flag(arguments, expected):
    parser = argparse.ArgumentParser()
    spack.cmd.install.setup_parser(parser)
    args = parser.parse_args(arguments)
    assert args.dirty == expected


def test_package_output(tmpdir, capsys, install_mockery, mock_fetch):
    """
    Ensure output printed from pkgs is captured by output redirection.
    """
    # we can't use output capture here because it interferes with Spack's
    # logging. TODO: see whether we can get multiple log_outputs to work
    # when nested AND in pytest
    spec = Spec('printing-package').concretized()
    pkg = spec.package
    pkg.do_install(verbose=True)

    log_file = pkg.build_log_path
    with open(log_file) as f:
        out = f.read()

    # make sure that output from the actual package file appears in the
    # right place in the build log.
    assert "BEFORE INSTALL" in out
    assert "AFTER INSTALL" in out


@pytest.mark.disable_clean_stage_check
def test_install_output_on_build_error(mock_packages, mock_archive, mock_fetch,
                                       config, install_mockery, capfd):
    """
    This test used to assume receiving full output, but since we've updated
    spack to generate logs on the level of phases, it will only return the
    last phase, install.
    """
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        out = install('-v', 'build-error', fail_on_error=False)
    assert 'Installing build-error' in out


@pytest.mark.disable_clean_stage_check
def test_install_output_on_python_error(
        mock_packages, mock_archive, mock_fetch, config, install_mockery):
    out = install('failing-build', fail_on_error=False)
    assert isinstance(install.error, spack.build_environment.ChildError)
    assert install.error.name == 'InstallError'
    assert 'raise InstallError("Expected failure.")' in out


@pytest.mark.disable_clean_stage_check
def test_install_with_source(
        mock_packages, mock_archive, mock_fetch, config, install_mockery):
    """Verify that source has been copied into place."""
    install('--source', '--keep-stage', 'trivial-install-test-package')
    spec = Spec('trivial-install-test-package').concretized()
    src = os.path.join(
        spec.prefix.share, 'trivial-install-test-package', 'src')
    assert filecmp.cmp(os.path.join(mock_archive.path, 'configure'),
                       os.path.join(src, 'configure'))


def test_install_env_variables(
    mock_packages, mock_archive, mock_fetch, config, install_mockery
):
    spec = Spec('libdwarf')
    spec.concretize()
    install('libdwarf')
    assert os.path.isfile(spec.package.install_env_path)


@pytest.mark.disable_clean_stage_check
def test_show_log_on_error(mock_packages, mock_archive, mock_fetch,
                           config, install_mockery, capfd):
    """
    Make sure --show-log-on-error works.
    """
    with capfd.disabled():
        out = install('--show-log-on-error', 'build-error',
                      fail_on_error=False)
    assert isinstance(install.error, spack.build_environment.ChildError)
    assert install.error.pkg.name == 'build-error'

    assert '==> Installing build-error' in out
    assert 'See build log for details:' in out


def test_install_overwrite(
        mock_packages, mock_archive, mock_fetch, config, install_mockery
):
    # Try to install a spec and then to reinstall it.
    spec = Spec('libdwarf')
    spec.concretize()

    install('libdwarf')

    # Ignore manifest and install times
    manifest = os.path.join(spec.prefix, spack.store.layout.metadata_dir,
                            spack.store.layout.manifest_file_name)
    ignores = [manifest, spec.package.times_log_path]

    assert os.path.exists(spec.prefix)
    expected_md5 = fs.hash_directory(spec.prefix, ignore=ignores)

    # Modify the first installation to be sure the content is not the same
    # as the one after we reinstalled
    with open(os.path.join(spec.prefix, 'only_in_old'), 'w') as f:
        f.write('This content is here to differentiate installations.')

    bad_md5 = fs.hash_directory(spec.prefix, ignore=ignores)

    assert bad_md5 != expected_md5

    install('--overwrite', '-y', 'libdwarf')

    assert os.path.exists(spec.prefix)
    assert fs.hash_directory(spec.prefix, ignore=ignores) == expected_md5
    assert fs.hash_directory(spec.prefix, ignore=ignores) != bad_md5


def test_install_overwrite_not_installed(
        mock_packages, mock_archive, mock_fetch, config, install_mockery,
):
    # Try to install a spec and then to reinstall it.
    spec = Spec('libdwarf')
    spec.concretize()

    assert not os.path.exists(spec.prefix)

    install('--overwrite', '-y', 'libdwarf')
    assert os.path.exists(spec.prefix)


def test_install_commit(
        mock_git_version_info, install_mockery, mock_packages, monkeypatch):
    """
    Test installing a git package from a commit.

    This ensures Spack appropriately associates commit versions with their
    packages in time to do version lookups. Details of version lookup tested elsewhere
    """
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(spack.package.PackageBase,
                        'git', 'file://%s' % repo_path,
                        raising=False)

    commit = commits[-1]
    spec = spack.spec.Spec('git-test-commit@%s' % commit)
    spec.concretize()
    spec.package.do_install()

    # Ensure first commit file contents were written
    installed = os.listdir(spec.prefix.bin)
    assert filename in installed
    with open(spec.prefix.bin.join(filename), 'r') as f:
        content = f.read().strip()
    assert content == '[]'  # contents are weird for another test


def test_install_overwrite_multiple(
        mock_packages, mock_archive, mock_fetch, config, install_mockery
):
    # Try to install a spec and then to reinstall it.
    libdwarf = Spec('libdwarf')
    libdwarf.concretize()

    install('libdwarf')

    cmake = Spec('cmake')
    cmake.concretize()

    install('cmake')

    ld_manifest = os.path.join(libdwarf.prefix,
                               spack.store.layout.metadata_dir,
                               spack.store.layout.manifest_file_name)

    ld_ignores = [ld_manifest, libdwarf.package.times_log_path]

    assert os.path.exists(libdwarf.prefix)
    expected_libdwarf_md5 = fs.hash_directory(libdwarf.prefix,
                                              ignore=ld_ignores)

    cm_manifest = os.path.join(cmake.prefix,
                               spack.store.layout.metadata_dir,
                               spack.store.layout.manifest_file_name)

    cm_ignores = [cm_manifest, cmake.package.times_log_path]
    assert os.path.exists(cmake.prefix)
    expected_cmake_md5 = fs.hash_directory(cmake.prefix, ignore=cm_ignores)

    # Modify the first installation to be sure the content is not the same
    # as the one after we reinstalled
    with open(os.path.join(libdwarf.prefix, 'only_in_old'), 'w') as f:
        f.write('This content is here to differentiate installations.')
    with open(os.path.join(cmake.prefix, 'only_in_old'), 'w') as f:
        f.write('This content is here to differentiate installations.')

    bad_libdwarf_md5 = fs.hash_directory(libdwarf.prefix, ignore=ld_ignores)
    bad_cmake_md5 = fs.hash_directory(cmake.prefix, ignore=cm_ignores)

    assert bad_libdwarf_md5 != expected_libdwarf_md5
    assert bad_cmake_md5 != expected_cmake_md5

    install('--overwrite', '-y', 'libdwarf', 'cmake')
    assert os.path.exists(libdwarf.prefix)
    assert os.path.exists(cmake.prefix)

    ld_hash = fs.hash_directory(libdwarf.prefix, ignore=ld_ignores)
    cm_hash = fs.hash_directory(cmake.prefix, ignore=cm_ignores)
    assert ld_hash == expected_libdwarf_md5
    assert cm_hash == expected_cmake_md5
    assert ld_hash != bad_libdwarf_md5
    assert cm_hash != bad_cmake_md5


@pytest.mark.usefixtures(
    'mock_packages', 'mock_archive', 'mock_fetch', 'config', 'install_mockery',
)
def test_install_conflicts(conflict_spec):
    # Make sure that spec with conflicts raises a SpackError
    with pytest.raises(SpackError):
        install(conflict_spec)


@pytest.mark.usefixtures(
    'mock_packages', 'mock_archive', 'mock_fetch', 'config', 'install_mockery',
)
def test_install_invalid_spec(invalid_spec):
    # Make sure that invalid specs raise a SpackError
    with pytest.raises(SpackError, match='Unexpected token'):
        install(invalid_spec)


@pytest.mark.usefixtures('noop_install', 'mock_packages', 'config')
@pytest.mark.parametrize('spec,concretize,error_code', [
    (Spec('mpi'), False, 1),
    (Spec('mpi'), True, 0),
    (Spec('boost'), False, 1),
    (Spec('boost'), True, 0)
])
def test_install_from_file(spec, concretize, error_code, tmpdir):

    if concretize:
        spec.concretize()

    specfile = tmpdir.join('spec.yaml')

    with specfile.open('w') as f:
        spec.to_yaml(f)

    err_msg = 'does not contain a concrete spec' if error_code else ''

    # Relative path to specfile (regression for #6906)
    with fs.working_dir(specfile.dirname):
        # A non-concrete spec will fail to be installed
        out = install('-f', specfile.basename, fail_on_error=False)
    assert install.returncode == error_code
    assert err_msg in out

    # Absolute path to specfile (regression for #6983)
    out = install('-f', str(specfile), fail_on_error=False)
    assert install.returncode == error_code
    assert err_msg in out


@pytest.mark.disable_clean_stage_check
@pytest.mark.usefixtures(
    'mock_packages', 'mock_archive', 'mock_fetch', 'config', 'install_mockery'
)
@pytest.mark.parametrize('exc_typename,msg', [
    ('RuntimeError', 'something weird happened'),
    ('ValueError', 'spec is not concrete')
])
def test_junit_output_with_failures(tmpdir, exc_typename, msg):
    with tmpdir.as_cwd():
        install(
            '--log-format=junit', '--log-file=test.xml',
            'raiser',
            'exc_type={0}'.format(exc_typename),
            'msg="{0}"'.format(msg)
        )

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()

    # Count failures and errors correctly
    assert 'tests="1"' in content
    assert 'failures="1"' in content
    assert 'errors="0"' in content

    # We want to have both stdout and stderr
    assert '<system-out>' in content
    assert msg in content


@pytest.mark.disable_clean_stage_check
@pytest.mark.parametrize('exc_typename,msg', [
    ('RuntimeError', 'something weird happened'),
    ('KeyboardInterrupt', 'Ctrl-C strikes again')
])
def test_junit_output_with_errors(
        exc_typename, msg,
        mock_packages, mock_archive, mock_fetch, install_mockery,
        config, tmpdir, monkeypatch):

    def just_throw(*args, **kwargs):
        exc_type = getattr(builtins, exc_typename)
        raise exc_type(msg)

    monkeypatch.setattr(spack.installer.PackageInstaller, '_install_task',
                        just_throw)

    # TODO: Why does junit output capture appear to swallow the exception
    # TODO: as evidenced by the two failing packages getting tagged as
    # TODO: installed?
    with tmpdir.as_cwd():
        install('--log-format=junit', '--log-file=test.xml', 'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()

    # Count failures and errors correctly: libdwarf _and_ libelf
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="2"' in content

    # We want to have both stdout and stderr
    assert '<system-out>' in content
    assert 'error message="{0}"'.format(msg) in content


@pytest.mark.usefixtures('noop_install', 'mock_packages', 'config')
@pytest.mark.parametrize('clispecs,filespecs', [
    [[],                  ['mpi']],
    [[],                  ['mpi', 'boost']],
    [['cmake'],           ['mpi']],
    [['cmake', 'libelf'], []],
    [['cmake', 'libelf'], ['mpi', 'boost']],
])
def test_install_mix_cli_and_files(clispecs, filespecs, tmpdir):

    args = clispecs

    for spec in filespecs:
        filepath = tmpdir.join(spec + '.yaml')
        args = ['-f', str(filepath)] + args
        s = Spec(spec)
        s.concretize()
        with filepath.open('w') as f:
            s.to_yaml(f)

    install(*args, fail_on_error=False)
    assert install.returncode == 0


def test_extra_files_are_archived(mock_packages, mock_archive, mock_fetch,
                                  config, install_mockery):
    s = Spec('archive-files')
    s.concretize()

    install('archive-files')

    archive_dir = os.path.join(
        spack.store.layout.metadata_path(s), 'archived-files'
    )
    config_log = os.path.join(archive_dir,
                              mock_archive.expanded_archive_basedir,
                              'config.log')
    assert os.path.exists(config_log)

    errors_txt = os.path.join(archive_dir, 'errors.txt')
    assert os.path.exists(errors_txt)


@pytest.mark.disable_clean_stage_check
def test_cdash_report_concretization_error(tmpdir, mock_fetch, install_mockery,
                                           capfd, conflict_spec):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        with tmpdir.as_cwd():
            with pytest.raises(SpackError):
                install(
                    '--log-format=cdash',
                    '--log-file=cdash_reports',
                    conflict_spec)
            report_dir = tmpdir.join('cdash_reports')
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join('Update.xml')
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert '<UpdateReturnStatus>' in content
            # The message is different based on using the
            # new or the old concretizer
            expected_messages = (
                'Conflicts in concretized spec',
                'A conflict was triggered',
            )
            assert any(x in content for x in expected_messages)


@pytest.mark.disable_clean_stage_check
def test_cdash_upload_build_error(tmpdir, mock_fetch, install_mockery,
                                  capfd):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        with tmpdir.as_cwd():
            with pytest.raises(SpackError):
                install(
                    '--log-format=cdash',
                    '--log-file=cdash_reports',
                    '--cdash-upload-url=http://localhost/fakeurl/submit.php?project=Spack',
                    'build-error')
            report_dir = tmpdir.join('cdash_reports')
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join('Build.xml')
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert '<Text>configure: error: in /path/to/some/file:</Text>' in content


@pytest.mark.disable_clean_stage_check
def test_cdash_upload_clean_build(tmpdir, mock_fetch, install_mockery, capfd):
    # capfd interferes with Spack's capturing of e.g., Build.xml output
    with capfd.disabled():
        with tmpdir.as_cwd():
            install(
                '--log-file=cdash_reports',
                '--log-format=cdash',
                'a')
            report_dir = tmpdir.join('cdash_reports')
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join('a_Build.xml')
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert '</Build>' in content
            assert '<Text>' not in content


@pytest.mark.disable_clean_stage_check
def test_cdash_upload_extra_params(tmpdir, mock_fetch, install_mockery, capfd):
    # capfd interferes with Spack's capture of e.g., Build.xml output
    with capfd.disabled():
        with tmpdir.as_cwd():
            install(
                '--log-file=cdash_reports',
                '--log-format=cdash',
                '--cdash-build=my_custom_build',
                '--cdash-site=my_custom_site',
                '--cdash-track=my_custom_track',
                'a')
            report_dir = tmpdir.join('cdash_reports')
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join('a_Build.xml')
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert 'Site BuildName="my_custom_build - a"' in content
            assert 'Name="my_custom_site"' in content
            assert '-my_custom_track' in content


@pytest.mark.disable_clean_stage_check
def test_cdash_buildstamp_param(tmpdir, mock_fetch, install_mockery, capfd):
    # capfd interferes with Spack's capture of e.g., Build.xml output
    with capfd.disabled():
        with tmpdir.as_cwd():
            cdash_track = 'some_mocked_track'
            buildstamp_format = "%Y%m%d-%H%M-{0}".format(cdash_track)
            buildstamp = time.strftime(buildstamp_format,
                                       time.localtime(int(time.time())))
            install(
                '--log-file=cdash_reports',
                '--log-format=cdash',
                '--cdash-buildstamp={0}'.format(buildstamp),
                'a')
            report_dir = tmpdir.join('cdash_reports')
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join('a_Build.xml')
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert buildstamp in content


@pytest.mark.disable_clean_stage_check
def test_cdash_install_from_spec_yaml(tmpdir, mock_fetch, install_mockery,
                                      capfd, mock_packages, mock_archive,
                                      config):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        with tmpdir.as_cwd():

            spec_yaml_path = str(tmpdir.join('spec.yaml'))

            pkg_spec = Spec('a')
            pkg_spec.concretize()

            with open(spec_yaml_path, 'w') as fd:
                fd.write(pkg_spec.to_yaml(hash=ht.build_hash))

            install(
                '--log-format=cdash',
                '--log-file=cdash_reports',
                '--cdash-build=my_custom_build',
                '--cdash-site=my_custom_site',
                '--cdash-track=my_custom_track',
                '-f', spec_yaml_path)

            report_dir = tmpdir.join('cdash_reports')
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join('a_Configure.xml')
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            install_command_regex = re.compile(
                r'<ConfigureCommand>(.+)</ConfigureCommand>',
                re.MULTILINE | re.DOTALL)
            m = install_command_regex.search(content)
            assert m
            install_command = m.group(1)
            assert 'a@' in install_command


@pytest.mark.disable_clean_stage_check
def test_build_error_output(tmpdir, mock_fetch, install_mockery, capfd):
    with capfd.disabled():
        msg = ''
        try:
            install('build-error')
            assert False, "no exception was raised!"
        except spack.build_environment.ChildError as e:
            msg = e.long_message

        assert 'configure: error: in /path/to/some/file:' in msg
        assert 'configure: error: cannot run C compiled programs.' in msg


@pytest.mark.disable_clean_stage_check
def test_build_warning_output(tmpdir, mock_fetch, install_mockery, capfd):
    with capfd.disabled():
        msg = ''
        try:
            install('build-warnings')
            assert False, "no exception was raised!"
        except spack.build_environment.ChildError as e:
            msg = e.long_message

        assert 'WARNING: ALL CAPITAL WARNING!' in msg
        assert 'foo.c:89: warning: some weird warning!' in msg


def test_cache_only_fails(tmpdir, mock_fetch, install_mockery, capfd):
    # libelf from cache fails to install, which automatically removes the
    # the libdwarf build task
    with capfd.disabled():
        out = install('--cache-only', 'libdwarf', fail_on_error=False)

    assert 'Failed to install libelf' in out
    assert 'Skipping build of libdwarf' in out
    assert 'was not installed' in out

    # Check that failure prefix locks are still cached
    failure_lock_prefixes = ','.join(spack.store.db._prefix_failures.keys())
    assert 'libelf' in failure_lock_prefixes
    assert 'libdwarf' in failure_lock_prefixes


def test_install_only_dependencies(tmpdir, mock_fetch, install_mockery):
    dep = Spec('dependency-install').concretized()
    root = Spec('dependent-install').concretized()

    install('--only', 'dependencies', 'dependent-install')

    assert os.path.exists(dep.prefix)
    assert not os.path.exists(root.prefix)


def test_install_only_package(tmpdir, mock_fetch, install_mockery, capfd):
    msg = ''
    with capfd.disabled():
        try:
            install('--only', 'package', 'dependent-install')
        except spack.installer.InstallError as e:
            msg = str(e)

    assert 'Cannot proceed with dependent-install'  in msg
    assert '1 uninstalled dependency' in msg


def test_install_deps_then_package(tmpdir, mock_fetch, install_mockery):
    dep = Spec('dependency-install').concretized()
    root = Spec('dependent-install').concretized()

    install('--only', 'dependencies', 'dependent-install')
    assert os.path.exists(dep.prefix)
    assert not os.path.exists(root.prefix)

    install('--only', 'package', 'dependent-install')
    assert os.path.exists(root.prefix)


@pytest.mark.regression('12002')
def test_install_only_dependencies_in_env(tmpdir, mock_fetch, install_mockery,
                                          mutable_mock_env_path):
    env('create', 'test')

    with ev.read('test'):
        dep = Spec('dependency-install').concretized()
        root = Spec('dependent-install').concretized()

        install('-v', '--only', 'dependencies', 'dependent-install')

        assert os.path.exists(dep.prefix)
        assert not os.path.exists(root.prefix)


@pytest.mark.regression('12002')
def test_install_only_dependencies_of_all_in_env(
    tmpdir, mock_fetch, install_mockery, mutable_mock_env_path
):
    env('create', '--without-view', 'test')

    with ev.read('test'):
        roots = [Spec('dependent-install@1.0').concretized(),
                 Spec('dependent-install@2.0').concretized()]

        add('dependent-install@1.0')
        add('dependent-install@2.0')
        install('--only', 'dependencies')

        for root in roots:
            assert not os.path.exists(root.prefix)
            for dep in root.traverse(root=False):
                assert os.path.exists(dep.prefix)


def test_install_no_add_in_env(tmpdir, mock_fetch, install_mockery,
                               mutable_mock_env_path):
    # To test behavior of --no-add option, we create the following environment:
    #
    #     mpileaks
    #         ^callpath
    #             ^dyninst
    #                 ^libelf@0.8.13     # or latest, really
    #                 ^libdwarf
    #         ^mpich
    #     libelf@0.8.10
    #     a~bvv
    #         ^b
    #     a
    #         ^b
    e = ev.create('test')
    e.add('mpileaks')
    e.add('libelf@0.8.10')  # so env has both root and dep libelf specs
    e.add('a')
    e.add('a ~bvv')
    e.concretize()
    env_specs = e.all_specs()

    a_spec = None
    b_spec = None
    mpi_spec = None

    # First find and remember some target concrete specs in the environment
    for e_spec in env_specs:
        if e_spec.satisfies(Spec('a ~bvv')):
            a_spec = e_spec
        elif e_spec.name == 'b':
            b_spec = e_spec
        elif e_spec.satisfies(Spec('mpi')):
            mpi_spec = e_spec

    assert(a_spec)
    assert(a_spec.concrete)

    assert(b_spec)
    assert(b_spec.concrete)
    assert(b_spec not in e.roots())

    assert(mpi_spec)
    assert(mpi_spec.concrete)

    # Activate the environment
    with e:
        # Assert using --no-add with a spec not in the env fails
        inst_out = install(
            '--no-add', 'boost', fail_on_error=False, output=str)

        assert('no such spec exists in environment' in inst_out)

        # Ensure using --no-add with an ambiguous spec fails
        with pytest.raises(ev.SpackEnvironmentError) as err:
            inst_out = install(
                '--no-add', 'a', output=str)

        assert('a matches multiple specs in the env' in str(err))

        # With "--no-add", install an unambiguous dependency spec (that already
        # exists as a dep in the environment) using --no-add and make sure it
        # gets installed (w/ deps), but is not added to the environment.
        install('--no-add', 'dyninst')

        find_output = find('-l', output=str)
        assert('dyninst' in find_output)
        assert('libdwarf' in find_output)
        assert('libelf' in find_output)
        assert('callpath' not in find_output)

        post_install_specs = e.all_specs()
        assert all([s in env_specs for s in post_install_specs])

        # Make sure we can install a concrete dependency spec from a spec.yaml
        # file on disk, using the ``--no-add` option, and the spec is installed
        # but not added as a root
        mpi_spec_yaml_path = tmpdir.join('{0}.yaml'.format(mpi_spec.name))
        with open(mpi_spec_yaml_path.strpath, 'w') as fd:
            fd.write(mpi_spec.to_yaml(hash=ht.full_hash))

        install('--no-add', '-f', mpi_spec_yaml_path.strpath)
        assert(mpi_spec not in e.roots())

        find_output = find('-l', output=str)
        assert(mpi_spec.name in find_output)

        # Without "--no-add", install an unambiguous depependency spec (that
        # already exists as a dep in the environment) without --no-add and make
        # sure it is added as a root of the environment as well as installed.
        assert(b_spec not in e.roots())

        install('b')

        assert(b_spec in e.roots())
        assert(b_spec not in e.uninstalled_specs())

        # Without "--no-add", install a novel spec and make sure it is added
        # as a root and installed.
        install('bowtie')

        assert(any([s.name == 'bowtie' for s in e.roots()]))
        assert(not any([s.name == 'bowtie' for s in e.uninstalled_specs()]))


def test_install_help_does_not_show_cdash_options(capsys):
    """
    Make sure `spack install --help` does not describe CDash arguments
    """
    with pytest.raises(SystemExit):
        install('--help')
        captured = capsys.readouterr()
        assert 'CDash URL' not in captured.out


def test_install_help_cdash(capsys):
    """Make sure `spack install --help-cdash` describes CDash arguments"""
    install_cmd = SpackCommand('install')
    out = install_cmd('--help-cdash')
    assert 'CDash URL' in out


@pytest.mark.disable_clean_stage_check
def test_cdash_auth_token(tmpdir, install_mockery, capfd):
    # capfd interferes with Spack's capturing
    with tmpdir.as_cwd():
        with capfd.disabled():
            os.environ['SPACK_CDASH_AUTH_TOKEN'] = 'asdf'
            out = install(
                '-v',
                '--log-file=cdash_reports',
                '--log-format=cdash',
                'a')
            assert 'Using CDash auth token from environment' in out


@pytest.mark.disable_clean_stage_check
def test_cdash_configure_warning(tmpdir, mock_fetch, install_mockery, capfd):
    # capfd interferes with Spack's capturing of e.g., Build.xml output
    with capfd.disabled():
        with tmpdir.as_cwd():
            # Test would fail if install raised an error.
            install(
                '--log-file=cdash_reports',
                '--log-format=cdash',
                'configure-warning')
            # Verify Configure.xml exists with expected contents.
            report_dir = tmpdir.join('cdash_reports')
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join('Configure.xml')
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert 'foo: No such file or directory' in content


def test_compiler_bootstrap(
        install_mockery_mutable_config, mock_packages, mock_fetch,
        mock_archive, mutable_config, monkeypatch):
    monkeypatch.setattr(spack.concretize.Concretizer,
                        'check_for_compiler_existence', False)
    spack.config.set('config:install_missing_compilers', True)
    assert CompilerSpec('gcc@2.0') not in compilers.all_compiler_specs()

    # Test succeeds if it does not raise an error
    install('a%gcc@2.0')


def test_compiler_bootstrap_from_binary_mirror(
        install_mockery_mutable_config, mock_packages, mock_fetch,
        mock_archive, mutable_config, monkeypatch, tmpdir):
    """
    Make sure installing compiler from buildcache registers compiler
    """

    # Create a temp mirror directory for buildcache usage
    mirror_dir = tmpdir.join('mirror_dir')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    # Install a compiler, because we want to put it in a buildcache
    install('gcc@10.2.0')

    # Put installed compiler in the buildcache
    buildcache(
        'create', '-u', '-a', '-f', '-d', mirror_dir.strpath, 'gcc@10.2.0'
    )

    # Now uninstall the compiler
    uninstall('-y', 'gcc@10.2.0')

    monkeypatch.setattr(spack.concretize.Concretizer,
                        'check_for_compiler_existence', False)
    spack.config.set('config:install_missing_compilers', True)
    assert CompilerSpec('gcc@10.2.0') not in compilers.all_compiler_specs()

    # Configure the mirror where we put that buildcache w/ the compiler
    mirror('add', 'test-mirror', mirror_url)

    # Now make sure that when the compiler is installed from binary mirror,
    # it also gets configured as a compiler.  Test succeeds if it does not
    # raise an error
    install('--no-check-signature', '--cache-only', '--only',
            'dependencies', 'b%gcc@10.2.0')
    install('--no-cache', '--only', 'package', 'b%gcc@10.2.0')


@pytest.mark.regression('16221')
def test_compiler_bootstrap_already_installed(
        install_mockery_mutable_config, mock_packages, mock_fetch,
        mock_archive, mutable_config, monkeypatch):
    monkeypatch.setattr(spack.concretize.Concretizer,
                        'check_for_compiler_existence', False)
    spack.config.set('config:install_missing_compilers', True)

    assert CompilerSpec('gcc@2.0') not in compilers.all_compiler_specs()

    # Test succeeds if it does not raise an error
    install('gcc@2.0')
    install('a%gcc@2.0')


def test_install_fails_no_args(tmpdir):
    # ensure no spack.yaml in directory
    with tmpdir.as_cwd():
        output = install(fail_on_error=False)

    # check we got the short version of the error message with no spack.yaml
    assert 'requires a package argument or active environment' in output
    assert 'spack env activate .' not in output
    assert 'using the `spack.yaml` in this directory' not in output


def test_install_fails_no_args_suggests_env_activation(tmpdir):
    # ensure spack.yaml in directory
    tmpdir.ensure('spack.yaml')

    with tmpdir.as_cwd():
        output = install(fail_on_error=False)

    # check we got the long version of the error message with spack.yaml
    assert 'requires a package argument or active environment' in output
    assert 'spack env activate .' in output
    assert 'using the `spack.yaml` in this directory' in output


default_full_hash = spack.spec.Spec.full_hash


def fake_full_hash(spec):
    # Generate an arbitrary hash that is intended to be different than
    # whatever a Spec reported before (to test actions that trigger when
    # the hash changes)
    if spec.name == 'libdwarf':
        return 'tal4c7h4z0gqmixb1eqa92mjoybxn5l6'
    return default_full_hash(spec)


def test_cache_install_full_hash_match(
        install_mockery_mutable_config, mock_packages, mock_fetch,
        mock_archive, mutable_config, monkeypatch, tmpdir):
    """Make sure installing from cache respects full hash argument"""

    # Create a temp mirror directory for buildcache usage
    mirror_dir = tmpdir.join('mirror_dir')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    s = Spec('libdwarf').concretized()
    package_id = spack.installer.package_id(s.package)

    # Install a package
    install(s.name)

    # Put installed package in the buildcache
    buildcache('create', '-u', '-a', '-f', '-d', mirror_dir.strpath, s.name)

    # Now uninstall the package
    uninstall('-y', s.name)

    # Configure the mirror with the binary package in it
    mirror('add', 'test-mirror', mirror_url)

    # Make sure we get the binary version by default
    install_output = install('--no-check-signature', s.name, output=str)
    expect_extract_msg = 'Extracting {0} from binary cache'.format(package_id)

    assert expect_extract_msg in install_output

    uninstall('-y', s.name)

    # Now monkey patch Spec to change the full hash on the package
    monkeypatch.setattr(spack.spec.Spec, 'full_hash', fake_full_hash)

    # Check that even if the full hash changes, we install from binary when
    # we don't explicitly require the full hash to match
    install_output = install('--no-check-signature', s.name, output=str)
    assert expect_extract_msg in install_output

    uninstall('-y', s.name)

    # Finally, make sure that if we insist on the full hash match, spack
    # installs from source.
    install_output = install('--require-full-hash-match', s.name, output=str)
    expect_msg = 'No binary for {0} found: installing from source'.format(
        package_id)

    assert expect_msg in install_output

    uninstall('-y', s.name)
    mirror('rm', 'test-mirror')

    # Get rid of that libdwarf binary in the mirror so other tests don't try to
    # use it and fail because of NoVerifyException
    shutil.rmtree(mirror_dir.strpath)


def test_install_env_with_tests_all(tmpdir, mock_packages, mock_fetch,
                                    install_mockery, mutable_mock_env_path):
    env('create', 'test')
    with ev.read('test'):
        test_dep = Spec('test-dependency').concretized()
        add('depb')
        install('--test', 'all')
        assert os.path.exists(test_dep.prefix)


def test_install_env_with_tests_root(tmpdir, mock_packages, mock_fetch,
                                     install_mockery, mutable_mock_env_path):
    env('create', 'test')
    with ev.read('test'):
        test_dep = Spec('test-dependency').concretized()
        add('depb')
        install('--test', 'root')
        assert not os.path.exists(test_dep.prefix)
