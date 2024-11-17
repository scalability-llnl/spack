# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

import pytest

import llnl.util.filesystem as fs

import spack.build_environment
import spack.config
import spack.database
import spack.error
import spack.installer
import spack.mirror
import spack.package_base
import spack.patch
import spack.repo
import spack.store
import spack.util.spack_json as sjson
from spack import binary_distribution
from spack.error import InstallError
from spack.installer import PackageInstaller
from spack.package_base import (
    PackageBase,
    PackageStillNeededError,
    _spack_build_envfile,
    _spack_build_logfile,
    _spack_configure_argsfile,
    spack_times_log,
)
from spack.spec import Spec


def find_nothing(*args):
    raise spack.repo.UnknownPackageError("Repo package access is disabled for test")


def test_install_and_uninstall(install_mockery, mock_fetch, monkeypatch):
    spec = Spec("trivial-install-test-package").concretized()

    PackageInstaller([spec.package], explicit=True).install()
    assert spec.installed

    spec.package.do_uninstall()
    assert not spec.installed


@pytest.mark.regression("11870")
def test_uninstall_non_existing_package(install_mockery, mock_fetch, monkeypatch):
    """Ensure that we can uninstall a package that has been deleted from the repo"""
    spec = Spec("trivial-install-test-package").concretized()

    PackageInstaller([spec.package], explicit=True).install()
    assert spec.installed

    # Mock deletion of the package
    spec._package = None
    monkeypatch.setattr(spack.repo.PATH, "get", find_nothing)
    with pytest.raises(spack.repo.UnknownPackageError):
        spec.package

    # Ensure we can uninstall it
    PackageBase.uninstall_by_spec(spec)
    assert not spec.installed


def test_pkg_attributes(install_mockery, mock_fetch, monkeypatch):
    # Get a basic concrete spec for the dummy package.
    spec = Spec("attributes-foo-app ^attributes-foo")
    spec.concretize()
    assert spec.concrete

    pkg = spec.package
    PackageInstaller([pkg], explicit=True).install()
    foo = "attributes-foo"
    assert spec["bar"].prefix == spec[foo].prefix
    assert spec["baz"].prefix == spec[foo].prefix

    assert spec[foo].home == spec[foo].prefix
    assert spec["bar"].home == spec[foo].home
    assert spec["baz"].home == spec[foo].prefix.baz

    foo_headers = spec[foo].headers
    # assert foo_headers.basenames == ['foo.h']
    assert foo_headers.directories == [spec[foo].home.include]
    bar_headers = spec["bar"].headers
    # assert bar_headers.basenames == ['bar.h']
    assert bar_headers.directories == [spec["bar"].home.include]
    baz_headers = spec["baz"].headers
    # assert baz_headers.basenames == ['baz.h']
    assert baz_headers.directories == [spec["baz"].home.include]

    lib_suffix = ".so"
    if sys.platform == "win32":
        lib_suffix = ".dll"
    elif sys.platform == "darwin":
        lib_suffix = ".dylib"

    foo_libs = spec[foo].libs
    assert foo_libs.basenames == ["libFoo" + lib_suffix]
    assert foo_libs.directories == [spec[foo].home.lib64]
    bar_libs = spec["bar"].libs
    assert bar_libs.basenames == ["libFooBar" + lib_suffix]
    assert bar_libs.directories == [spec["bar"].home.lib64]
    baz_libs = spec["baz"].libs
    assert baz_libs.basenames == ["libFooBaz" + lib_suffix]
    assert baz_libs.directories == [spec["baz"].home.lib]


def mock_remove_prefix(*args):
    raise MockInstallError("Intentional error", "Mock remove_prefix method intentionally fails")


class RemovePrefixChecker:
    def __init__(self, wrapped_rm_prefix):
        self.removed = False
        self.wrapped_rm_prefix = wrapped_rm_prefix

    def remove_prefix(self):
        self.removed = True
        self.wrapped_rm_prefix()


def test_partial_install_delete_prefix_and_stage(install_mockery, mock_fetch, working_env):
    s = Spec("canfail").concretized()

    instance_rm_prefix = s.package.remove_prefix

    s.package.remove_prefix = mock_remove_prefix
    with pytest.raises(MockInstallError):
        PackageInstaller([s.package], explicit=True).install()
    assert os.path.isdir(s.package.prefix)
    rm_prefix_checker = RemovePrefixChecker(instance_rm_prefix)
    s.package.remove_prefix = rm_prefix_checker.remove_prefix

    # must clear failure markings for the package before re-installing it
    spack.store.STORE.failure_tracker.clear(s, True)

    s.package.set_install_succeed()
    PackageInstaller([s.package], explicit=True, restage=True).install()
    assert rm_prefix_checker.removed
    assert s.package.spec.installed


@pytest.mark.not_on_windows("Fails spuriously on Windows")
@pytest.mark.disable_clean_stage_check
def test_failing_overwrite_install_should_keep_previous_installation(
    mock_fetch, install_mockery, working_env
):
    """
    Make sure that whenever `spack install --overwrite` fails, spack restores
    the original install prefix instead of cleaning it.
    """
    # Do a successful install
    s = Spec("canfail").concretized()
    s.package.set_install_succeed()

    # Do a failing overwrite install
    PackageInstaller([s.package], explicit=True).install()
    s.package.set_install_fail()
    kwargs = {"overwrite": [s.dag_hash()]}

    with pytest.raises(Exception):
        PackageInstaller([s.package], explicit=True, **kwargs).install()

    assert s.package.spec.installed
    assert os.path.exists(s.prefix)


def test_dont_add_patches_to_installed_package(install_mockery, mock_fetch, monkeypatch):
    dependency = Spec("dependency-install")
    dependency.concretize()
    PackageInstaller([dependency.package], explicit=True).install()

    dependency_hash = dependency.dag_hash()
    dependent = Spec("dependent-install ^/" + dependency_hash)
    dependent.concretize()

    monkeypatch.setitem(
        dependency.package.patches,
        "dependency-install",
        [spack.patch.UrlPatch(dependent.package, "file://fake.patch", sha256="unused-hash")],
    )

    assert dependent["dependency-install"] == dependency


def test_installed_dependency_request_conflicts(install_mockery, mock_fetch, mutable_mock_repo):
    dependency = Spec("dependency-install")
    dependency.concretize()
    PackageInstaller([dependency.package], explicit=True).install()

    dependency_hash = dependency.dag_hash()
    dependent = Spec("conflicting-dependent ^/" + dependency_hash)
    with pytest.raises(spack.error.UnsatisfiableSpecError):
        dependent.concretize()


def test_install_dependency_symlinks_pkg(install_mockery, mock_fetch, mutable_mock_repo):
    """Test dependency flattening/symlinks mock package."""
    spec = Spec("flatten-deps")
    spec.concretize()
    pkg = spec.package
    PackageInstaller([pkg], explicit=True).install()

    # Ensure dependency directory exists after the installation.
    dependency_dir = os.path.join(pkg.prefix, "dependency-install")
    assert os.path.isdir(dependency_dir)


def test_install_times(install_mockery, mock_fetch, mutable_mock_repo):
    """Test install times added."""
    spec = Spec("dev-build-test-install-phases").concretized()
    PackageInstaller([spec.package], explicit=True).install()

    # Ensure dependency directory exists after the installation.
    install_times = os.path.join(spec.package.prefix, ".spack", spack_times_log)
    assert os.path.isfile(install_times)

    # Ensure the phases are included
    with open(install_times, "r") as timefile:
        times = sjson.load(timefile.read())

    # The order should be maintained
    phases = [x["name"] for x in times["phases"]]
    assert phases == ["stage", "one", "two", "three", "install", "post-install"]
    assert all(isinstance(x["seconds"], float) for x in times["phases"])


def test_flatten_deps(install_mockery, mock_fetch, mutable_mock_repo):
    """Explicitly test the flattening code for coverage purposes."""
    # Unfortunately, executing the 'flatten-deps' spec's installation does
    # not affect code coverage results, so be explicit here.
    spec = Spec("dependent-install")
    spec.concretize()
    pkg = spec.package
    PackageInstaller([pkg], explicit=True).install()

    # Demonstrate that the directory does not appear under the spec
    # prior to the flatten operation.
    dependency_name = "dependency-install"
    assert dependency_name not in os.listdir(pkg.prefix)

    # Flatten the dependencies and ensure the dependency directory is there.
    spack.package_base.flatten_dependencies(spec, pkg.prefix)

    dependency_dir = os.path.join(pkg.prefix, dependency_name)
    assert os.path.isdir(dependency_dir)


@pytest.fixture()
def install_upstream(tmpdir_factory, gen_mock_layout, install_mockery):
    """Provides a function that installs a specified set of specs to an
    upstream database. The function returns a store which points to the
    upstream, as well as the upstream layout (for verifying that dependent
    installs are using the upstream installs).
    """
    mock_db_root = str(tmpdir_factory.mktemp("mock_db_root"))
    upstream_layout = gen_mock_layout("/a/")
    prepared_db = spack.database.Database(mock_db_root, layout=upstream_layout)
    spack.config.CONFIG.push_scope(
        spack.config.InternalConfigScope(
            name="install-upstream-fixture",
            data={"upstreams": {"mock1": {"install_tree": prepared_db.root}}},
        )
    )

    def _install_upstream(*specs):
        for spec_str in specs:
            prepared_db.add(Spec(spec_str).concretized())
        downstream_root = str(tmpdir_factory.mktemp("mock_downstream_db_root"))
        return downstream_root, upstream_layout

    return _install_upstream


def test_installed_upstream_external(install_upstream, mock_fetch):
    """Check that when a dependency package is recorded as installed in
    an upstream database that it is not reinstalled.
    """
    store_root, _ = install_upstream("externaltool")
    with spack.store.use_store(store_root):
        dependent = Spec("externaltest")
        dependent.concretize()

        new_dependency = dependent["externaltool"]
        assert new_dependency.external
        assert new_dependency.prefix == os.path.sep + os.path.join("path", "to", "external_tool")

        PackageInstaller([dependent.package], explicit=True).install()

        assert not os.path.exists(new_dependency.prefix)
        assert os.path.exists(dependent.prefix)


def test_installed_upstream(install_upstream, mock_fetch):
    """Check that when a dependency package is recorded as installed in
    an upstream database that it is not reinstalled.
    """
    store_root, upstream_layout = install_upstream("dependency-install")
    with spack.store.use_store(store_root):
        dependency = Spec("dependency-install").concretized()
        dependent = Spec("dependent-install").concretized()

        new_dependency = dependent["dependency-install"]
        assert new_dependency.installed_upstream
        assert new_dependency.prefix == upstream_layout.path_for_spec(dependency)

        PackageInstaller([dependent.package], explicit=True).install()

        assert not os.path.exists(new_dependency.prefix)
        assert os.path.exists(dependent.prefix)


@pytest.mark.disable_clean_stage_check
def test_partial_install_keep_prefix(install_mockery, mock_fetch, monkeypatch, working_env):
    s = Spec("canfail").concretized()

    # If remove_prefix is called at any point in this test, that is an error
    monkeypatch.setattr(spack.package_base.PackageBase, "remove_prefix", mock_remove_prefix)
    with pytest.raises(spack.build_environment.ChildError):
        PackageInstaller([s.package], explicit=True, keep_prefix=True).install()
    assert os.path.exists(s.package.prefix)

    # must clear failure markings for the package before re-installing it
    spack.store.STORE.failure_tracker.clear(s, True)

    s.package.set_install_succeed()
    PackageInstaller([s.package], explicit=True, keep_prefix=True).install()
    assert s.package.spec.installed


def test_second_install_no_overwrite_first(install_mockery, mock_fetch, monkeypatch):
    s = Spec("canfail").concretized()
    monkeypatch.setattr(spack.package_base.PackageBase, "remove_prefix", mock_remove_prefix)

    s.package.set_install_succeed()
    PackageInstaller([s.package], explicit=True).install()
    assert s.package.spec.installed

    # If Package.install is called after this point, it will fail
    s.package.set_install_fail()
    PackageInstaller([s.package], explicit=True).install()


def test_install_prefix_collision_fails(config, mock_fetch, mock_packages, tmpdir):
    """
    Test that different specs with coinciding install prefixes will fail
    to install.
    """
    projections = {"projections": {"all": "one-prefix-per-package-{name}"}}
    with spack.store.use_store(str(tmpdir), extra_data=projections):
        with spack.config.override("config:checksum", False):
            pkg_a = Spec("libelf@0.8.13").concretized().package
            pkg_b = Spec("libelf@0.8.12").concretized().package
            PackageInstaller([pkg_a], explicit=True, fake=True).install()

            with pytest.raises(InstallError, match="Install prefix collision"):
                PackageInstaller([pkg_b], explicit=True, fake=True).install()


def test_store(install_mockery, mock_fetch):
    spec = Spec("cmake-client").concretized()
    pkg = spec.package
    PackageInstaller([pkg], fake=True, explicit=True).install()


@pytest.mark.disable_clean_stage_check
def test_failing_build(install_mockery, mock_fetch, capfd):
    spec = Spec("failing-build").concretized()
    pkg = spec.package

    with pytest.raises(spack.build_environment.ChildError, match="Expected failure"):
        PackageInstaller([pkg], explicit=True).install()


class MockInstallError(spack.error.SpackError):
    pass


def test_uninstall_by_spec_errors(mutable_database):
    """Test exceptional cases with the uninstall command."""

    # Try to uninstall a spec that has not been installed
    spec = Spec("dependent-install")
    spec.concretize()
    with pytest.raises(InstallError, match="is not installed"):
        PackageBase.uninstall_by_spec(spec)

    # Try an unforced uninstall of a spec with dependencies
    rec = mutable_database.get_record("mpich")
    with pytest.raises(PackageStillNeededError, match="Cannot uninstall"):
        PackageBase.uninstall_by_spec(rec.spec)


@pytest.mark.disable_clean_stage_check
def test_nosource_pkg_install(install_mockery, mock_fetch, mock_packages, capfd, ensure_debug):
    """Test install phases with the nosource package."""
    spec = Spec("nosource").concretized()
    pkg = spec.package

    # Make sure install works even though there is no associated code.
    PackageInstaller([pkg], explicit=True).install()
    out = capfd.readouterr()
    assert "Installing dependency-install" in out[0]

    # Make sure a warning for missing code is issued
    assert "Missing a source id for nosource" in out[1]


@pytest.mark.disable_clean_stage_check
def test_nosource_bundle_pkg_install(
    install_mockery, mock_fetch, mock_packages, capfd, ensure_debug
):
    """Test install phases with the nosource-bundle package."""
    spec = Spec("nosource-bundle").concretized()
    pkg = spec.package

    # Make sure install works even though there is no associated code.
    PackageInstaller([pkg], explicit=True).install()
    out = capfd.readouterr()
    assert "Installing dependency-install" in out[0]

    # Make sure a warning for missing code is *not* issued
    assert "Missing a source id for nosource" not in out[1]


def test_nosource_pkg_install_post_install(install_mockery, mock_fetch, mock_packages):
    """Test install phases with the nosource package with post-install."""
    spec = Spec("nosource-install").concretized()
    pkg = spec.package

    # Make sure both the install and post-install package methods work.
    PackageInstaller([pkg], explicit=True).install()

    # Ensure the file created in the package's `install` method exists.
    install_txt = os.path.join(spec.prefix, "install.txt")
    assert os.path.isfile(install_txt)

    # Ensure the file created in the package's `post-install` method exists.
    post_install_txt = os.path.join(spec.prefix, "post-install.txt")
    assert os.path.isfile(post_install_txt)


def test_pkg_build_paths(install_mockery):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec("trivial-install-test-package").concretized()
    assert spec.package.log_path.endswith(_spack_build_logfile)
    assert spec.package.env_path.endswith(_spack_build_envfile)


def test_pkg_install_paths(install_mockery):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec("trivial-install-test-package").concretized()

    log_path = os.path.join(spec.prefix, ".spack", _spack_build_logfile + ".gz")
    assert spec.package.install_log_path == log_path

    env_path = os.path.join(spec.prefix, ".spack", _spack_build_envfile)
    assert spec.package.install_env_path == env_path

    args_path = os.path.join(spec.prefix, ".spack", _spack_configure_argsfile)
    assert spec.package.install_configure_args_path == args_path

    # Backward compatibility checks
    log_dir = os.path.dirname(log_path)
    fs.mkdirp(log_dir)
    with fs.working_dir(log_dir):
        # Start with the older of the previous install log filenames
        older_log = "build.out"
        fs.touch(older_log)
        assert spec.package.install_log_path.endswith(older_log)

        # Now check the newer install log filename
        last_log = "build.txt"
        fs.rename(older_log, last_log)
        assert spec.package.install_log_path.endswith(last_log)

        # Check the old install environment file
        last_env = "build.env"
        fs.rename(last_log, last_env)
        assert spec.package.install_env_path.endswith(last_env)

    # Cleanup
    shutil.rmtree(log_dir)


def test_log_install_without_build_files(install_mockery):
    """Test the installer log function when no build files are present."""
    # Get a basic concrete spec for the trivial install package.
    spec = Spec("trivial-install-test-package").concretized()

    # Attempt installing log without the build log file
    with pytest.raises(IOError, match="No such file or directory"):
        spack.installer.log(spec.package)


def test_log_install_with_build_files(install_mockery, monkeypatch):
    """Test the installer's log function when have build files."""
    config_log = "config.log"

    # Retain the original function for use in the monkey patch that is used
    # to raise an exception under the desired condition for test coverage.
    orig_install_fn = fs.install

    def _install(src, dest):
        orig_install_fn(src, dest)
        if src.endswith(config_log):
            raise Exception("Mock log install error")

    monkeypatch.setattr(fs, "install", _install)

    spec = Spec("trivial-install-test-package").concretized()

    # Set up mock build files and try again to include archive failure
    log_path = spec.package.log_path
    log_dir = os.path.dirname(log_path)
    fs.mkdirp(log_dir)
    with fs.working_dir(log_dir):
        fs.touch(log_path)
        fs.touch(spec.package.env_path)
        fs.touch(spec.package.env_mods_path)
        fs.touch(spec.package.configure_args_path)

    install_path = os.path.dirname(spec.package.install_log_path)
    fs.mkdirp(install_path)

    source = spec.package.stage.source_path
    config = os.path.join(source, "config.log")
    fs.touchp(config)
    monkeypatch.setattr(
        type(spec.package), "archive_files", ["missing", "..", config], raising=False
    )

    spack.installer.log(spec.package)

    assert os.path.exists(spec.package.install_log_path)
    assert os.path.exists(spec.package.install_env_path)
    assert os.path.exists(spec.package.install_configure_args_path)

    archive_dir = os.path.join(install_path, "archived-files")
    source_dir = os.path.dirname(source)
    rel_config = os.path.relpath(config, source_dir)

    assert os.path.exists(os.path.join(archive_dir, rel_config))
    assert not os.path.exists(os.path.join(archive_dir, "missing"))

    expected_errs = ["OUTSIDE SOURCE PATH", "FAILED TO ARCHIVE"]  # for '..'  # for rel_config
    with open(os.path.join(archive_dir, "errors.txt"), "r") as fd:
        for ln, expected in zip(fd, expected_errs):
            assert expected in ln

    # Cleanup
    shutil.rmtree(log_dir)


def test_unconcretized_install(install_mockery, mock_fetch, mock_packages):
    """Test attempts to perform install phases with unconcretized spec."""
    spec = Spec("trivial-install-test-package")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)

    with pytest.raises(ValueError, match="must have a concrete spec"):
        PackageInstaller([pkg_cls(spec)], explicit=True).install()

    with pytest.raises(ValueError, match="only patch concrete packages"):
        pkg_cls(spec).do_patch()


def test_install_error():
    try:
        msg = "test install error"
        long_msg = "this is the long version of test install error"
        raise InstallError(msg, long_msg=long_msg)
    except Exception as exc:
        assert exc.__class__.__name__ == "InstallError"
        assert exc.message == msg
        assert exc.long_message == long_msg


@pytest.mark.disable_clean_stage_check
def test_empty_install_sanity_check_prefix(
    monkeypatch, install_mockery, mock_fetch, mock_packages
):
    """Test empty install triggers sanity_check_prefix."""
    spec = Spec("failing-empty-install").concretized()
    with pytest.raises(spack.build_environment.ChildError, match="Nothing was installed"):
        PackageInstaller([spec.package], explicit=True).install()


def test_install_from_binary_with_missing_patch_succeeds(
    temporary_store: spack.store.Store, mutable_config, tmp_path, mock_packages
):
    """If a patch is missing in the local package repository, but was present when building and
    pushing the package to a binary cache, installation from that binary cache shouldn't error out
    because of the missing patch."""
    # Create a spec s with non-existing patches
    s = Spec("trivial-install-test-package").concretized()
    patches = ["a" * 64]
    s_dict = s.to_dict()
    s_dict["spec"]["nodes"][0]["patches"] = patches
    s_dict["spec"]["nodes"][0]["parameters"]["patches"] = patches
    s = Spec.from_dict(s_dict)

    # Create an install dir for it
    os.makedirs(os.path.join(s.prefix, ".spack"))
    with open(os.path.join(s.prefix, ".spack", "spec.json"), "w") as f:
        s.to_json(f)

    # And register it in the database
    temporary_store.db.add(s, explicit=True)

    # Push it to a binary cache
    mirror = spack.mirror.Mirror.from_local_path(str(tmp_path / "my_build_cache"))
    with binary_distribution.make_uploader(mirror=mirror) as uploader:
        uploader.push_or_raise([s])

    # Now re-install it.
    s.package.do_uninstall()
    assert not temporary_store.db.query_local_by_spec_hash(s.dag_hash())

    # Source install: fails, we don't have the patch.
    with pytest.raises(spack.error.SpecError, match="Couldn't find patch for package"):
        PackageInstaller([s.package], explicit=True).install()

    # Binary install: succeeds, we don't need the patch.
    spack.mirror.add(mirror)
    PackageInstaller(
        [s.package],
        explicit=True,
        package_cache_only=True,
        dependencies_cache_only=True,
        unsigned=True,
    ).install()

    assert temporary_store.db.query_local_by_spec_hash(s.dag_hash())
