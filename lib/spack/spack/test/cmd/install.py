# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import filecmp
import re
from six.moves import builtins
import time

import pytest

import llnl.util.filesystem as fs

import spack.config
import spack.compilers as compilers
import spack.hash_types as ht
import spack.package
import spack.cmd.install
from spack.error import SpackError
from spack.spec import Spec, CompilerSpec
from spack.main import SpackCommand
import spack.environment as ev

from six.moves.urllib.error import HTTPError, URLError

install = SpackCommand('install')
env = SpackCommand('env')
add = SpackCommand('add')


@pytest.fixture()
def noop_install(monkeypatch):
    def noop(*args, **kwargs):
        pass
    monkeypatch.setattr(spack.package.PackageBase, 'do_install', noop)


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


def test_global_install_package_and_dependency(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):

    with tmpdir.as_cwd():
        install('--global',
                '--log-format=junit',
                '--log-file=test.xml',
                'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content


def test_upstream_install_package_and_dependency(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):

    with tmpdir.as_cwd():
        install('--upstream=global',
                '--log-format=junit',
                '--log-file=test.xml',
                'libdwarf')

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
    """Ensure output printed from pkgs is captured by output redirection."""
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
    assert re.search(r"BEFORE INSTALL\n==>( \[.+\])? './configure'", out)
    assert "'install'\nAFTER INSTALL" in out


@pytest.mark.disable_clean_stage_check
def test_install_output_on_build_error(mock_packages, mock_archive, mock_fetch,
                                       config, install_mockery, capfd):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        out = install('build-error', fail_on_error=False)
    assert 'ProcessError' in out
    assert 'configure: error: in /path/to/some/file:' in out
    assert 'configure: error: cannot run C compiled programs.' in out


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


@pytest.mark.disable_clean_stage_check
def test_show_log_on_error(mock_packages, mock_archive, mock_fetch,
                           config, install_mockery, capfd):
    """Make sure --show-log-on-error works."""
    with capfd.disabled():
        out = install('--show-log-on-error', 'build-error',
                      fail_on_error=False)
    assert isinstance(install.error, spack.build_environment.ChildError)
    assert install.error.pkg.name == 'build-error'
    assert 'Full build log:' in out

    # Message shows up for ProcessError (1), ChildError (1), and output (1)
    errors = [line for line in out.split('\n')
              if 'configure: error: cannot run C compiled programs' in line]
    assert len(errors) == 3


def test_install_overwrite(
        mock_packages, mock_archive, mock_fetch, config, install_mockery
):
    # Try to install a spec and then to reinstall it.
    spec = Spec('libdwarf')
    spec.concretize()

    install('libdwarf')

    manifest = os.path.join(spec.prefix, spack.store.layout.metadata_dir,
                            spack.store.layout.manifest_file_name)

    assert os.path.exists(spec.prefix)
    expected_md5 = fs.hash_directory(spec.prefix, ignore=[manifest])

    # Modify the first installation to be sure the content is not the same
    # as the one after we reinstalled
    with open(os.path.join(spec.prefix, 'only_in_old'), 'w') as f:
        f.write('This content is here to differentiate installations.')

    bad_md5 = fs.hash_directory(spec.prefix, ignore=[manifest])

    assert bad_md5 != expected_md5

    install('--overwrite', '-y', 'libdwarf')

    assert os.path.exists(spec.prefix)
    assert fs.hash_directory(spec.prefix, ignore=[manifest]) == expected_md5
    assert fs.hash_directory(spec.prefix, ignore=[manifest]) != bad_md5


def test_install_overwrite_not_installed(
        mock_packages, mock_archive, mock_fetch, config, install_mockery
):
    # Try to install a spec and then to reinstall it.
    spec = Spec('libdwarf')
    spec.concretize()

    assert not os.path.exists(spec.prefix)

    install('--overwrite', '-y', 'libdwarf')
    assert os.path.exists(spec.prefix)


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

    assert os.path.exists(libdwarf.prefix)
    expected_libdwarf_md5 = fs.hash_directory(libdwarf.prefix,
                                              ignore=[ld_manifest])

    cm_manifest = os.path.join(cmake.prefix,
                               spack.store.layout.metadata_dir,
                               spack.store.layout.manifest_file_name)

    assert os.path.exists(cmake.prefix)
    expected_cmake_md5 = fs.hash_directory(cmake.prefix, ignore=[cm_manifest])

    # Modify the first installation to be sure the content is not the same
    # as the one after we reinstalled
    with open(os.path.join(libdwarf.prefix, 'only_in_old'), 'w') as f:
        f.write('This content is here to differentiate installations.')
    with open(os.path.join(cmake.prefix, 'only_in_old'), 'w') as f:
        f.write('This content is here to differentiate installations.')

    bad_libdwarf_md5 = fs.hash_directory(libdwarf.prefix, ignore=[ld_manifest])
    bad_cmake_md5 = fs.hash_directory(cmake.prefix, ignore=[cm_manifest])

    assert bad_libdwarf_md5 != expected_libdwarf_md5
    assert bad_cmake_md5 != expected_cmake_md5

    install('--overwrite', '-y', 'libdwarf', 'cmake')
    assert os.path.exists(libdwarf.prefix)
    assert os.path.exists(cmake.prefix)

    ld_hash = fs.hash_directory(libdwarf.prefix, ignore=[ld_manifest])
    cm_hash = fs.hash_directory(cmake.prefix, ignore=[cm_manifest])
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


@pytest.mark.usefixtures('noop_install', 'config')
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

    # Relative path to specfile (regression for #6906)
    with fs.working_dir(specfile.dirname):
        # A non-concrete spec will fail to be installed
        install('-f', specfile.basename, fail_on_error=False)
    assert install.returncode == error_code

    # Absolute path to specfile (regression for #6983)
    install('-f', str(specfile), fail_on_error=False)
    assert install.returncode == error_code


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


@pytest.mark.usefixtures('noop_install', 'config')
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
            assert '<UpdateReturnStatus>Conflicts in concretized spec' \
                in content


@pytest.mark.disable_clean_stage_check
def test_cdash_upload_build_error(tmpdir, mock_fetch, install_mockery,
                                  capfd):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        with tmpdir.as_cwd():
            with pytest.raises((HTTPError, URLError)):
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


def test_cache_only_fails(tmpdir, mock_fetch, install_mockery):
    # libelf from cache fails to install, which automatically removes the
    # the libdwarf build task and flags the package as failed to install.
    err_msg = 'Installation of libdwarf failed'
    with pytest.raises(spack.installer.InstallError, match=err_msg):
        install('--cache-only', 'libdwarf')

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


def test_install_help_does_not_show_cdash_options(capsys):
    """Make sure `spack install --help` does not describe CDash arguments"""
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


def test_compiler_bootstrap(
        install_mockery_mutable_config, mock_packages, mock_fetch,
        mock_archive, mutable_config, monkeypatch):
    monkeypatch.setattr(spack.concretize.Concretizer,
                        'check_for_compiler_existence', False)
    spack.config.set('config:install_missing_compilers', True)
    assert CompilerSpec('gcc@2.0') not in compilers.all_compiler_specs()

    # Test succeeds if it does not raise an error
    install('a%gcc@2.0')


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
