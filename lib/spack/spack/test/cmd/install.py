# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import builtins
import filecmp
import gzip
import itertools
import os
import pathlib
import re
import time

import pytest

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.build_environment
import spack.cmd.common.arguments
import spack.cmd.install
import spack.config
import spack.environment as ev
import spack.error
import spack.hash_types as ht
import spack.installer
import spack.package_base
import spack.store
from spack.error import SpackError, SpecSyntaxError
from spack.installer import PackageInstaller
from spack.main import SpackCommand
from spack.spec import Spec

install = SpackCommand("install")
env = SpackCommand("env")
add = SpackCommand("add")
mirror = SpackCommand("mirror")
uninstall = SpackCommand("uninstall")
buildcache = SpackCommand("buildcache")
find = SpackCommand("find")


@pytest.fixture()
def noop_install(monkeypatch):
    def noop(*args, **kwargs):
        pass

    monkeypatch.setattr(spack.installer.PackageInstaller, "install", noop)


def test_install_package_and_dependency(
    tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery
):
    log = "test"
    with tmpdir.as_cwd():
        install("--log-format=junit", "--log-file={0}".format(log), "libdwarf")

    files = tmpdir.listdir()
    filename = tmpdir.join("{0}.xml".format(log))
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content


@pytest.mark.disable_clean_stage_check
def test_install_runtests_notests(monkeypatch, mock_packages, install_mockery):
    def check(pkg):
        assert not pkg.run_tests

    monkeypatch.setattr(spack.package_base.PackageBase, "unit_test_check", check)
    install("-v", "dttop")


@pytest.mark.disable_clean_stage_check
def test_install_runtests_root(monkeypatch, mock_packages, install_mockery):
    def check(pkg):
        assert pkg.run_tests == (pkg.name == "dttop")

    monkeypatch.setattr(spack.package_base.PackageBase, "unit_test_check", check)
    install("--test=root", "dttop")


@pytest.mark.disable_clean_stage_check
def test_install_runtests_all(monkeypatch, mock_packages, install_mockery):
    def check(pkg):
        assert pkg.run_tests

    monkeypatch.setattr(spack.package_base.PackageBase, "unit_test_check", check)
    install("--test=all", "pkg-a")


def test_install_package_already_installed(
    tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery
):
    with tmpdir.as_cwd():
        install("libdwarf")
        install("--log-format=junit", "--log-file=test.xml", "libdwarf")

    files = tmpdir.listdir()
    filename = tmpdir.join("test.xml")
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content

    skipped = [line for line in content.split("\n") if "skipped" in line]
    assert len(skipped) == 2


@pytest.mark.parametrize(
    "arguments,expected",
    [
        ([], spack.config.get("config:dirty")),  # default from config file
        (["--clean"], False),
        (["--dirty"], True),
    ],
)
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
    spec = Spec("printing-package").concretized()
    pkg = spec.package
    PackageInstaller([pkg], explicit=True, verbose=True).install()

    with gzip.open(pkg.install_log_path, "rt") as f:
        out = f.read()

    # make sure that output from the actual package file appears in the
    # right place in the build log.
    assert "BEFORE INSTALL" in out
    assert "AFTER INSTALL" in out


@pytest.mark.disable_clean_stage_check
def test_install_output_on_build_error(
    mock_packages, mock_archive, mock_fetch, install_mockery, capfd
):
    """
    This test used to assume receiving full output, but since we've updated
    spack to generate logs on the level of phases, it will only return the
    last phase, install.
    """
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        out = install("-v", "build-error", fail_on_error=False)
    assert "Installing build-error" in out


@pytest.mark.disable_clean_stage_check
def test_install_output_on_python_error(mock_packages, mock_archive, mock_fetch, install_mockery):
    out = install("failing-build", fail_on_error=False)
    assert isinstance(install.error, spack.build_environment.ChildError)
    assert install.error.name == "InstallError"
    assert 'raise InstallError("Expected failure.")' in out


@pytest.mark.disable_clean_stage_check
def test_install_with_source(mock_packages, mock_archive, mock_fetch, install_mockery):
    """Verify that source has been copied into place."""
    install("--source", "--keep-stage", "trivial-install-test-package")
    spec = Spec("trivial-install-test-package").concretized()
    src = os.path.join(spec.prefix.share, "trivial-install-test-package", "src")
    assert filecmp.cmp(
        os.path.join(mock_archive.path, "configure"), os.path.join(src, "configure")
    )


def test_install_env_variables(mock_packages, mock_archive, mock_fetch, install_mockery):
    spec = Spec("libdwarf")
    spec.concretize()
    install("libdwarf")
    assert os.path.isfile(spec.package.install_env_path)


@pytest.mark.disable_clean_stage_check
def test_show_log_on_error(mock_packages, mock_archive, mock_fetch, install_mockery, capfd):
    """
    Make sure --show-log-on-error works.
    """
    with capfd.disabled():
        out = install("--show-log-on-error", "build-error", fail_on_error=False)
    assert isinstance(install.error, spack.build_environment.ChildError)
    assert install.error.pkg.name == "build-error"

    assert "Installing build-error" in out
    assert "See build log for details:" in out


def test_install_overwrite(mock_packages, mock_archive, mock_fetch, install_mockery):
    # Try to install a spec and then to reinstall it.
    spec = Spec("libdwarf")
    spec.concretize()

    install("libdwarf")

    # Ignore manifest and install times
    manifest = os.path.join(
        spec.prefix,
        spack.store.STORE.layout.metadata_dir,
        spack.store.STORE.layout.manifest_file_name,
    )
    ignores = [manifest, spec.package.times_log_path]

    assert os.path.exists(spec.prefix)
    expected_md5 = fs.hash_directory(spec.prefix, ignore=ignores)

    # Modify the first installation to be sure the content is not the same
    # as the one after we reinstalled
    with open(os.path.join(spec.prefix, "only_in_old"), "w") as f:
        f.write("This content is here to differentiate installations.")

    bad_md5 = fs.hash_directory(spec.prefix, ignore=ignores)

    assert bad_md5 != expected_md5

    install("--overwrite", "-y", "libdwarf")

    assert os.path.exists(spec.prefix)
    assert fs.hash_directory(spec.prefix, ignore=ignores) == expected_md5
    assert fs.hash_directory(spec.prefix, ignore=ignores) != bad_md5


def test_install_overwrite_not_installed(mock_packages, mock_archive, mock_fetch, install_mockery):
    # Try to install a spec and then to reinstall it.
    spec = Spec("libdwarf")
    spec.concretize()

    assert not os.path.exists(spec.prefix)

    install("--overwrite", "-y", "libdwarf")
    assert os.path.exists(spec.prefix)


def test_install_commit(mock_git_version_info, install_mockery, mock_packages, monkeypatch):
    """Test installing a git package from a commit.

    This ensures Spack associates commit versions with their packages in time to do
    version lookups. Details of version lookup tested elsewhere.

    """
    repo_path, filename, commits = mock_git_version_info
    file_url = pathlib.Path(repo_path).as_uri()

    monkeypatch.setattr(spack.package_base.PackageBase, "git", file_url, raising=False)

    # Use the earliest commit in the respository
    spec = Spec(f"git-test-commit@{commits[-1]}").concretized()
    PackageInstaller([spec.package], explicit=True).install()

    # Ensure first commit file contents were written
    installed = os.listdir(spec.prefix.bin)
    assert filename in installed
    with open(spec.prefix.bin.join(filename), "r") as f:
        content = f.read().strip()
    assert content == "[0]"  # contents are weird for another test


def test_install_overwrite_multiple(mock_packages, mock_archive, mock_fetch, install_mockery):
    # Try to install a spec and then to reinstall it.
    libdwarf = Spec("libdwarf")
    libdwarf.concretize()

    install("libdwarf")

    cmake = Spec("cmake")
    cmake.concretize()

    install("cmake")

    ld_manifest = os.path.join(
        libdwarf.prefix,
        spack.store.STORE.layout.metadata_dir,
        spack.store.STORE.layout.manifest_file_name,
    )

    ld_ignores = [ld_manifest, libdwarf.package.times_log_path]

    assert os.path.exists(libdwarf.prefix)
    expected_libdwarf_md5 = fs.hash_directory(libdwarf.prefix, ignore=ld_ignores)

    cm_manifest = os.path.join(
        cmake.prefix,
        spack.store.STORE.layout.metadata_dir,
        spack.store.STORE.layout.manifest_file_name,
    )

    cm_ignores = [cm_manifest, cmake.package.times_log_path]
    assert os.path.exists(cmake.prefix)
    expected_cmake_md5 = fs.hash_directory(cmake.prefix, ignore=cm_ignores)

    # Modify the first installation to be sure the content is not the same
    # as the one after we reinstalled
    with open(os.path.join(libdwarf.prefix, "only_in_old"), "w") as f:
        f.write("This content is here to differentiate installations.")
    with open(os.path.join(cmake.prefix, "only_in_old"), "w") as f:
        f.write("This content is here to differentiate installations.")

    bad_libdwarf_md5 = fs.hash_directory(libdwarf.prefix, ignore=ld_ignores)
    bad_cmake_md5 = fs.hash_directory(cmake.prefix, ignore=cm_ignores)

    assert bad_libdwarf_md5 != expected_libdwarf_md5
    assert bad_cmake_md5 != expected_cmake_md5

    install("--overwrite", "-y", "libdwarf", "cmake")
    assert os.path.exists(libdwarf.prefix)
    assert os.path.exists(cmake.prefix)

    ld_hash = fs.hash_directory(libdwarf.prefix, ignore=ld_ignores)
    cm_hash = fs.hash_directory(cmake.prefix, ignore=cm_ignores)
    assert ld_hash == expected_libdwarf_md5
    assert cm_hash == expected_cmake_md5
    assert ld_hash != bad_libdwarf_md5
    assert cm_hash != bad_cmake_md5


@pytest.mark.usefixtures("mock_packages", "mock_archive", "mock_fetch", "install_mockery")
def test_install_conflicts(conflict_spec):
    # Make sure that spec with conflicts raises a SpackError
    with pytest.raises(SpackError):
        install(conflict_spec)


@pytest.mark.usefixtures("mock_packages", "mock_archive", "mock_fetch", "install_mockery")
def test_install_invalid_spec(invalid_spec):
    # Make sure that invalid specs raise a SpackError
    with pytest.raises(SpecSyntaxError, match="unexpected tokens"):
        install(invalid_spec)


@pytest.mark.usefixtures("noop_install", "mock_packages", "config")
@pytest.mark.parametrize(
    "spec,concretize,error_code",
    [
        (Spec("mpi"), False, 1),
        (Spec("mpi"), True, 0),
        (Spec("boost"), False, 1),
        (Spec("boost"), True, 0),
    ],
)
def test_install_from_file(spec, concretize, error_code, tmpdir):
    if concretize:
        spec.concretize()

    specfile = tmpdir.join("spec.yaml")

    with specfile.open("w") as f:
        spec.to_yaml(f)

    err_msg = "does not contain a concrete spec" if error_code else ""

    # Relative path to specfile (regression for #6906)
    with fs.working_dir(specfile.dirname):
        # A non-concrete spec will fail to be installed
        out = install("-f", specfile.basename, fail_on_error=False)
    assert install.returncode == error_code
    assert err_msg in out

    # Absolute path to specfile (regression for #6983)
    out = install("-f", str(specfile), fail_on_error=False)
    assert install.returncode == error_code
    assert err_msg in out


@pytest.mark.disable_clean_stage_check
@pytest.mark.usefixtures("mock_packages", "mock_archive", "mock_fetch", "install_mockery")
@pytest.mark.parametrize(
    "exc_typename,msg",
    [("RuntimeError", "something weird happened"), ("ValueError", "spec is not concrete")],
)
def test_junit_output_with_failures(tmpdir, exc_typename, msg):
    with tmpdir.as_cwd():
        install(
            "--log-format=junit",
            "--log-file=test.xml",
            "raiser",
            "exc_type={0}".format(exc_typename),
            'msg="{0}"'.format(msg),
            fail_on_error=False,
        )

    assert isinstance(install.error, spack.build_environment.ChildError)
    assert install.error.name == exc_typename
    assert install.error.pkg.name == "raiser"

    files = tmpdir.listdir()
    filename = tmpdir.join("test.xml")
    assert filename in files

    content = filename.open().read()

    # Count failures and errors correctly
    assert 'tests="1"' in content
    assert 'failures="1"' in content
    assert 'errors="0"' in content

    # Nothing should have succeeded
    assert 'tests="0"' not in content
    assert 'failures="0"' not in content

    # We want to have both stdout and stderr
    assert "<system-out>" in content
    assert msg in content


@pytest.mark.disable_clean_stage_check
@pytest.mark.parametrize(
    "exc_typename,expected_exc,msg",
    [
        ("RuntimeError", spack.error.InstallError, "something weird happened"),
        ("KeyboardInterrupt", KeyboardInterrupt, "Ctrl-C strikes again"),
    ],
)
def test_junit_output_with_errors(
    exc_typename,
    expected_exc,
    msg,
    mock_packages,
    mock_archive,
    mock_fetch,
    install_mockery,
    tmpdir,
    monkeypatch,
):
    def just_throw(*args, **kwargs):
        exc_type = getattr(builtins, exc_typename)
        raise exc_type(msg)

    monkeypatch.setattr(spack.installer.PackageInstaller, "_install_task", just_throw)

    with tmpdir.as_cwd():
        install("--log-format=junit", "--log-file=test.xml", "libdwarf", fail_on_error=False)

    assert isinstance(install.error, expected_exc)

    files = tmpdir.listdir()
    filename = tmpdir.join("test.xml")
    assert filename in files

    content = filename.open().read()

    # Only libelf error is reported (through libdwarf root spec). libdwarf
    # install is skipped and it is not an error.
    assert 'tests="1"' in content
    assert 'failures="0"' in content
    assert 'errors="1"' in content

    # Nothing should have succeeded
    assert 'errors="0"' not in content

    # We want to have both stdout and stderr
    assert "<system-out>" in content
    assert 'error message="{0}"'.format(msg) in content


@pytest.mark.usefixtures("noop_install", "mock_packages", "config")
@pytest.mark.parametrize(
    "clispecs,filespecs",
    [
        [[], ["mpi"]],
        [[], ["mpi", "boost"]],
        [["cmake"], ["mpi"]],
        [["cmake", "libelf"], []],
        [["cmake", "libelf"], ["mpi", "boost"]],
    ],
)
def test_install_mix_cli_and_files(clispecs, filespecs, tmpdir):
    args = clispecs

    for spec in filespecs:
        filepath = tmpdir.join(spec + ".yaml")
        args = ["-f", str(filepath)] + args
        s = Spec(spec)
        s.concretize()
        with filepath.open("w") as f:
            s.to_yaml(f)

    install(*args, fail_on_error=False)
    assert install.returncode == 0


def test_extra_files_are_archived(mock_packages, mock_archive, mock_fetch, install_mockery):
    s = Spec("archive-files")
    s.concretize()

    install("archive-files")

    archive_dir = os.path.join(spack.store.STORE.layout.metadata_path(s), "archived-files")
    config_log = os.path.join(archive_dir, mock_archive.expanded_archive_basedir, "config.log")
    assert os.path.exists(config_log)

    errors_txt = os.path.join(archive_dir, "errors.txt")
    assert os.path.exists(errors_txt)


@pytest.mark.disable_clean_stage_check
def test_cdash_report_concretization_error(
    tmpdir, mock_fetch, install_mockery, capfd, conflict_spec
):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        with tmpdir.as_cwd():
            with pytest.raises(SpackError):
                install("--log-format=cdash", "--log-file=cdash_reports", conflict_spec)
            report_dir = tmpdir.join("cdash_reports")
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join("Update.xml")
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert "<UpdateReturnStatus>" in content
            # The message is different based on using the
            # new or the old concretizer
            expected_messages = ("Conflicts in concretized spec", "conflicts with")
            assert any(x in content for x in expected_messages)


@pytest.mark.not_on_windows("Windows log_output logs phase header out of order")
@pytest.mark.disable_clean_stage_check
def test_cdash_upload_build_error(tmpdir, mock_fetch, install_mockery, capfd):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        with tmpdir.as_cwd():
            with pytest.raises(SpackError):
                install(
                    "--log-format=cdash",
                    "--log-file=cdash_reports",
                    "--cdash-upload-url=http://localhost/fakeurl/submit.php?project=Spack",
                    "build-error",
                )
            report_dir = tmpdir.join("cdash_reports")
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join("Build.xml")
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert "<Text>configure: error: in /path/to/some/file:</Text>" in content


@pytest.mark.disable_clean_stage_check
def test_cdash_upload_clean_build(tmpdir, mock_fetch, install_mockery, capfd):
    # capfd interferes with Spack's capturing of e.g., Build.xml output
    with capfd.disabled(), tmpdir.as_cwd():
        install("--log-file=cdash_reports", "--log-format=cdash", "pkg-a")
        report_dir = tmpdir.join("cdash_reports")
        assert report_dir in tmpdir.listdir()
        report_file = report_dir.join("pkg-a_Build.xml")
        assert report_file in report_dir.listdir()
        content = report_file.open().read()
        assert "</Build>" in content
        assert "<Text>" not in content


@pytest.mark.disable_clean_stage_check
def test_cdash_upload_extra_params(tmpdir, mock_fetch, install_mockery, capfd):
    # capfd interferes with Spack's capture of e.g., Build.xml output
    with capfd.disabled(), tmpdir.as_cwd():
        install(
            "--log-file=cdash_reports",
            "--log-format=cdash",
            "--cdash-build=my_custom_build",
            "--cdash-site=my_custom_site",
            "--cdash-track=my_custom_track",
            "pkg-a",
        )
        report_dir = tmpdir.join("cdash_reports")
        assert report_dir in tmpdir.listdir()
        report_file = report_dir.join("pkg-a_Build.xml")
        assert report_file in report_dir.listdir()
        content = report_file.open().read()
        assert 'Site BuildName="my_custom_build - pkg-a"' in content
        assert 'Name="my_custom_site"' in content
        assert "-my_custom_track" in content


@pytest.mark.disable_clean_stage_check
def test_cdash_buildstamp_param(tmpdir, mock_fetch, install_mockery, capfd):
    # capfd interferes with Spack's capture of e.g., Build.xml output
    with capfd.disabled(), tmpdir.as_cwd():
        cdash_track = "some_mocked_track"
        buildstamp_format = "%Y%m%d-%H%M-{0}".format(cdash_track)
        buildstamp = time.strftime(buildstamp_format, time.localtime(int(time.time())))
        install(
            "--log-file=cdash_reports",
            "--log-format=cdash",
            "--cdash-buildstamp={0}".format(buildstamp),
            "pkg-a",
        )
        report_dir = tmpdir.join("cdash_reports")
        assert report_dir in tmpdir.listdir()
        report_file = report_dir.join("pkg-a_Build.xml")
        assert report_file in report_dir.listdir()
        content = report_file.open().read()
        assert buildstamp in content


@pytest.mark.disable_clean_stage_check
def test_cdash_install_from_spec_json(
    tmpdir, mock_fetch, install_mockery, capfd, mock_packages, mock_archive
):
    # capfd interferes with Spack's capturing
    with capfd.disabled(), tmpdir.as_cwd():
        spec_json_path = str(tmpdir.join("spec.json"))

        pkg_spec = Spec("pkg-a")
        pkg_spec.concretize()

        with open(spec_json_path, "w") as fd:
            fd.write(pkg_spec.to_json(hash=ht.dag_hash))

        install(
            "--log-format=cdash",
            "--log-file=cdash_reports",
            "--cdash-build=my_custom_build",
            "--cdash-site=my_custom_site",
            "--cdash-track=my_custom_track",
            "-f",
            spec_json_path,
        )

        report_dir = tmpdir.join("cdash_reports")
        assert report_dir in tmpdir.listdir()
        report_file = report_dir.join("pkg-a_Configure.xml")
        assert report_file in report_dir.listdir()
        content = report_file.open().read()
        install_command_regex = re.compile(
            r"<ConfigureCommand>(.+)</ConfigureCommand>", re.MULTILINE | re.DOTALL
        )
        m = install_command_regex.search(content)
        assert m
        install_command = m.group(1)
        assert "pkg-a@" in install_command


@pytest.mark.disable_clean_stage_check
def test_build_error_output(tmpdir, mock_fetch, install_mockery, capfd):
    with capfd.disabled():
        msg = ""
        try:
            install("build-error")
            assert False, "no exception was raised!"
        except spack.build_environment.ChildError as e:
            msg = e.long_message

        assert "configure: error: in /path/to/some/file:" in msg
        assert "configure: error: cannot run C compiled programs." in msg


@pytest.mark.disable_clean_stage_check
def test_build_warning_output(tmpdir, mock_fetch, install_mockery, capfd):
    with capfd.disabled():
        msg = ""
        try:
            install("build-warnings")
            assert False, "no exception was raised!"
        except spack.build_environment.ChildError as e:
            msg = e.long_message

        assert "WARNING: ALL CAPITAL WARNING!" in msg
        assert "foo.c:89: warning: some weird warning!" in msg


def test_cache_only_fails(tmpdir, mock_fetch, install_mockery, capfd):
    # libelf from cache fails to install, which automatically removes the
    # the libdwarf build task
    with capfd.disabled():
        out = install("--cache-only", "libdwarf", fail_on_error=False)

    assert "Failed to install libelf" in out
    assert "Skipping build of libdwarf" in out
    assert "was not installed" in out

    # Check that failure prefix locks are still cached
    failed_packages = [
        pkg_name for dag_hash, pkg_name in spack.store.STORE.failure_tracker.locker.locks.keys()
    ]
    assert "libelf" in failed_packages
    assert "libdwarf" in failed_packages


def test_install_only_dependencies(tmpdir, mock_fetch, install_mockery):
    dep = Spec("dependency-install").concretized()
    root = Spec("dependent-install").concretized()

    install("--only", "dependencies", "dependent-install")

    assert os.path.exists(dep.prefix)
    assert not os.path.exists(root.prefix)


def test_install_only_package(tmpdir, mock_fetch, install_mockery, capfd):
    msg = ""
    with capfd.disabled():
        try:
            install("--only", "package", "dependent-install")
        except spack.error.InstallError as e:
            msg = str(e)

    assert "Cannot proceed with dependent-install" in msg
    assert "1 uninstalled dependency" in msg


def test_install_deps_then_package(tmpdir, mock_fetch, install_mockery):
    dep = Spec("dependency-install").concretized()
    root = Spec("dependent-install").concretized()

    install("--only", "dependencies", "dependent-install")
    assert os.path.exists(dep.prefix)
    assert not os.path.exists(root.prefix)

    install("--only", "package", "dependent-install")
    assert os.path.exists(root.prefix)


@pytest.mark.not_on_windows("Environment views not supported on windows. Revisit after #34701")
@pytest.mark.regression("12002")
def test_install_only_dependencies_in_env(
    tmpdir, mock_fetch, install_mockery, mutable_mock_env_path
):
    env("create", "test")

    with ev.read("test"):
        dep = Spec("dependency-install").concretized()
        root = Spec("dependent-install").concretized()

        install("-v", "--only", "dependencies", "--add", "dependent-install")

        assert os.path.exists(dep.prefix)
        assert not os.path.exists(root.prefix)


@pytest.mark.regression("12002")
def test_install_only_dependencies_of_all_in_env(
    tmpdir, mock_fetch, install_mockery, mutable_mock_env_path
):
    env("create", "--without-view", "test")

    with ev.read("test"):
        roots = [
            Spec("dependent-install@1.0").concretized(),
            Spec("dependent-install@2.0").concretized(),
        ]

        add("dependent-install@1.0")
        add("dependent-install@2.0")
        install("--only", "dependencies")

        for root in roots:
            assert not os.path.exists(root.prefix)
            for dep in root.traverse(root=False):
                assert os.path.exists(dep.prefix)


def test_install_no_add_in_env(tmpdir, mock_fetch, install_mockery, mutable_mock_env_path):
    # To test behavior of --add option, we create the following environment:
    #
    #     mpileaks
    #         ^callpath
    #             ^dyninst
    #                 ^libelf@0.8.13     # or latest, really
    #                 ^libdwarf
    #         ^mpich
    #     libelf@0.8.10
    #     pkg-a~bvv
    #         ^pkg-b
    #     pkg-a
    #         ^pkg-b
    e = ev.create("test", with_view=False)
    e.add("mpileaks")
    e.add("libelf@0.8.10")  # so env has both root and dep libelf specs
    e.add("pkg-a")
    e.add("pkg-a ~bvv")
    e.concretize()
    e.write()
    env_specs = e.all_specs()

    a_spec = None
    b_spec = None
    mpi_spec = None

    # First find and remember some target concrete specs in the environment
    for e_spec in env_specs:
        if e_spec.satisfies(Spec("pkg-a ~bvv")):
            a_spec = e_spec
        elif e_spec.name == "pkg-b":
            b_spec = e_spec
        elif e_spec.satisfies(Spec("mpi")):
            mpi_spec = e_spec

    assert a_spec
    assert a_spec.concrete

    assert b_spec
    assert b_spec.concrete
    assert b_spec not in e.roots()

    assert mpi_spec
    assert mpi_spec.concrete

    # Activate the environment
    with e:
        # Assert using --no-add with a spec not in the env fails
        inst_out = install("--no-add", "boost", fail_on_error=False, output=str)

        assert "You can add specs to the environment with 'spack add " in inst_out

        # Without --add, ensure that two packages "a" get installed
        inst_out = install("pkg-a", output=str)
        assert len([x for x in e.all_specs() if x.installed and x.name == "pkg-a"]) == 2

        # Install an unambiguous dependency spec (that already exists as a dep
        # in the environment) and make sure it gets installed (w/ deps),
        # but is not added to the environment.
        install("dyninst")

        find_output = find("-l", output=str)
        assert "dyninst" in find_output
        assert "libdwarf" in find_output
        assert "libelf" in find_output
        assert "callpath" not in find_output

        post_install_specs = e.all_specs()
        assert all([s in env_specs for s in post_install_specs])

        # Make sure we can install a concrete dependency spec from a spec.json
        # file on disk, and the spec is installed but not added as a root
        mpi_spec_json_path = tmpdir.join("{0}.json".format(mpi_spec.name))
        with open(mpi_spec_json_path.strpath, "w") as fd:
            fd.write(mpi_spec.to_json(hash=ht.dag_hash))

        install("-f", mpi_spec_json_path.strpath)
        assert mpi_spec not in e.roots()

        find_output = find("-l", output=str)
        assert mpi_spec.name in find_output

        # Install an unambiguous depependency spec (that already exists as a
        # dep in the environment) with --add and make sure it is added as a
        # root of the environment as well as installed.
        assert b_spec not in e.roots()

        install("--add", "pkg-b")

        assert b_spec in e.roots()
        assert b_spec not in e.uninstalled_specs()

        # Install a novel spec with --add and make sure it is added  as a root
        # and installed.
        install("--add", "bowtie")

        assert any([s.name == "bowtie" for s in e.roots()])
        assert not any([s.name == "bowtie" for s in e.uninstalled_specs()])


def test_install_help_does_not_show_cdash_options(capsys):
    """
    Make sure `spack install --help` does not describe CDash arguments
    """
    with pytest.raises(SystemExit):
        install("--help")
        captured = capsys.readouterr()
        assert "CDash URL" not in captured.out


def test_install_help_cdash():
    """Make sure `spack install --help-cdash` describes CDash arguments"""
    install_cmd = SpackCommand("install")
    out = install_cmd("--help-cdash")
    assert "CDash URL" in out


@pytest.mark.disable_clean_stage_check
def test_cdash_auth_token(tmpdir, mock_fetch, install_mockery, monkeypatch, capfd):
    # capfd interferes with Spack's capturing
    with tmpdir.as_cwd(), capfd.disabled():
        monkeypatch.setenv("SPACK_CDASH_AUTH_TOKEN", "asdf")
        out = install("-v", "--log-file=cdash_reports", "--log-format=cdash", "pkg-a")
        assert "Using CDash auth token from environment" in out


@pytest.mark.not_on_windows("Windows log_output logs phase header out of order")
@pytest.mark.disable_clean_stage_check
def test_cdash_configure_warning(tmpdir, mock_fetch, install_mockery, capfd):
    # capfd interferes with Spack's capturing of e.g., Build.xml output
    with capfd.disabled(), tmpdir.as_cwd():
        # Test would fail if install raised an error.

        # Ensure that even on non-x86_64 architectures, there are no
        # dependencies installed
        spec = Spec("configure-warning").concretized()
        spec.clear_dependencies()
        specfile = "./spec.json"
        with open(specfile, "w") as f:
            f.write(spec.to_json())

        install("--log-file=cdash_reports", "--log-format=cdash", specfile)
        # Verify Configure.xml exists with expected contents.
        report_dir = tmpdir.join("cdash_reports")
        assert report_dir in tmpdir.listdir()
        report_file = report_dir.join("Configure.xml")
        assert report_file in report_dir.listdir()
        content = report_file.open().read()
        assert "foo: No such file or directory" in content


def test_install_fails_no_args(tmpdir):
    # ensure no spack.yaml in directory
    with tmpdir.as_cwd():
        output = install(fail_on_error=False)

    # check we got the short version of the error message with no spack.yaml
    assert "requires a package argument or active environment" in output
    assert "spack env activate ." not in output
    assert "using the `spack.yaml` in this directory" not in output


def test_install_fails_no_args_suggests_env_activation(tmpdir):
    # ensure spack.yaml in directory
    tmpdir.ensure("spack.yaml")

    with tmpdir.as_cwd():
        output = install(fail_on_error=False)

    # check we got the long version of the error message with spack.yaml
    assert "requires a package argument or active environment" in output
    assert "spack env activate ." in output
    assert "using the `spack.yaml` in this directory" in output


@pytest.mark.not_on_windows("Environment views not supported on windows. Revisit after #34701")
def test_install_env_with_tests_all(
    tmpdir, mock_packages, mock_fetch, install_mockery, mutable_mock_env_path
):
    env("create", "test")
    with ev.read("test"):
        test_dep = Spec("test-dependency").concretized()
        add("depb")
        install("--test", "all")
        assert os.path.exists(test_dep.prefix)


@pytest.mark.not_on_windows("Environment views not supported on windows. Revisit after #34701")
def test_install_env_with_tests_root(
    tmpdir, mock_packages, mock_fetch, install_mockery, mutable_mock_env_path
):
    env("create", "test")
    with ev.read("test"):
        test_dep = Spec("test-dependency").concretized()
        add("depb")
        install("--test", "root")
        assert not os.path.exists(test_dep.prefix)


@pytest.mark.not_on_windows("Environment views not supported on windows. Revisit after #34701")
def test_install_empty_env(
    tmpdir, mock_packages, mock_fetch, install_mockery, mutable_mock_env_path
):
    env_name = "empty"
    env("create", env_name)
    with ev.read(env_name):
        out = install(fail_on_error=False)

    assert env_name in out
    assert "environment" in out
    assert "no specs to install" in out


@pytest.mark.not_on_windows("Windows logger I/O operation on closed file when install fails")
@pytest.mark.disable_clean_stage_check
@pytest.mark.parametrize(
    "name,method",
    [
        ("test-build-callbacks", "undefined-build-test"),
        ("test-install-callbacks", "undefined-install-test"),
    ],
)
def test_installation_fail_tests(install_mockery, mock_fetch, name, method):
    """Confirm build-time tests with unknown methods fail."""
    output = install("--test=root", "--no-cache", name, fail_on_error=False)

    # Check that there is a single test failure reported
    assert output.count("TestFailure: 1 test failed") == 1

    # Check that the method appears twice: no attribute error and in message
    assert output.count(method) == 2
    assert output.count("method not implemented") == 1

    # Check that the path to the test log file is also output
    assert "See test log for details" in output


@pytest.mark.not_on_windows("Buildcache not supported on windows")
def test_install_use_buildcache(
    capsys, mock_packages, mock_fetch, mock_archive, mock_binary_index, tmpdir, install_mockery
):
    """
    Make sure installing with use-buildcache behaves correctly.
    """

    package_name = "dependent-install"
    dependency_name = "dependency-install"

    def validate(mode, out, pkg):
        def assert_auto(pkg, out):
            assert "==> Extracting {0}".format(pkg) in out

        def assert_only(pkg, out):
            assert "==> Extracting {0}".format(pkg) in out

        def assert_never(pkg, out):
            assert "==> {0}: Executing phase: 'install'".format(pkg) in out

        if mode == "auto":
            assert_auto(pkg, out)
        elif mode == "only":
            assert_only(pkg, out)
        else:
            assert_never(pkg, out)

    def install_use_buildcache(opt):
        out = install(
            "--no-check-signature", "--use-buildcache", opt, package_name, fail_on_error=True
        )

        pkg_opt, dep_opt = spack.cmd.common.arguments.use_buildcache(opt)
        validate(dep_opt, out, dependency_name)
        validate(pkg_opt, out, package_name)

        # Clean up installed packages
        uninstall("-y", "-a")

    # Setup the mirror
    # Create a temp mirror directory for buildcache usage
    mirror_dir = tmpdir.join("mirror_dir")
    mirror_url = "file://{0}".format(mirror_dir.strpath)

    # Populate the buildcache
    install(package_name)
    buildcache("push", "-u", "-f", mirror_dir.strpath, package_name, dependency_name)

    # Uninstall the all of the packages for clean slate
    uninstall("-y", "-a")

    # Configure the mirror where we put that buildcache w/ the compiler
    mirror("add", "test-mirror", mirror_url)

    with capsys.disabled():
        # Install using the matrix of possible combinations with --use-buildcache
        for pkg, deps in itertools.product(["auto", "only", "never"], repeat=2):
            tty.debug(
                "Testing `spack install --use-buildcache package:{0},dependencies:{1}`".format(
                    pkg, deps
                )
            )
            install_use_buildcache("package:{0},dependencies:{1}".format(pkg, deps))
            install_use_buildcache("dependencies:{0},package:{1}".format(deps, pkg))

        # Install using a default override option
        # Alternative to --cache-only (always) or --no-cache (never)
        for opt in ["auto", "only", "never"]:
            install_use_buildcache(opt)


@pytest.mark.not_on_windows("Windows logger I/O operation on closed file when install fails")
@pytest.mark.regression("34006")
@pytest.mark.disable_clean_stage_check
def test_padded_install_runtests_root(install_mockery, mock_fetch):
    spack.config.set("config:install_tree:padded_length", 255)
    output = install("--test=root", "--no-cache", "test-build-callbacks", fail_on_error=False)
    assert output.count("method not implemented") == 1


@pytest.mark.regression("35337")
def test_report_filename_for_cdash(install_mockery, mock_fetch):
    """Test that the temporary file used to write the XML for CDash is not the upload URL"""
    parser = argparse.ArgumentParser()
    spack.cmd.install.setup_parser(parser)
    args = parser.parse_args(
        ["--cdash-upload-url", "https://blahblah/submit.php?project=debugging", "pkg-a"]
    )
    specs = spack.cmd.install.concrete_specs_from_cli(args, {})
    filename = spack.cmd.install.report_filename(args, specs)
    assert filename != "https://blahblah/submit.php?project=debugging"
