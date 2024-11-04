# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import json
import os
import shutil
from typing import List

import pytest

import spack.binary_distribution
import spack.cmd.buildcache
import spack.environment as ev
import spack.error
import spack.main
import spack.mirror
import spack.spec
import spack.util.url
from spack.installer import PackageInstaller
from spack.spec import Spec

buildcache = spack.main.SpackCommand("buildcache")
install = spack.main.SpackCommand("install")
env = spack.main.SpackCommand("env")
add = spack.main.SpackCommand("add")
gpg = spack.main.SpackCommand("gpg")
mirror = spack.main.SpackCommand("mirror")
uninstall = spack.main.SpackCommand("uninstall")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


@pytest.fixture()
def mock_get_specs(database, monkeypatch):
    specs = database.query_local()
    monkeypatch.setattr(spack.binary_distribution, "update_cache_and_get_specs", lambda: specs)


@pytest.fixture()
def mock_get_specs_multiarch(database, monkeypatch):
    specs = [spec.copy() for spec in database.query_local()]

    # make one spec that is NOT the test architecture
    for spec in specs:
        if spec.name == "mpileaks":
            spec.architecture = spack.spec.ArchSpec("linux-rhel7-x86_64")
            break

    monkeypatch.setattr(spack.binary_distribution, "update_cache_and_get_specs", lambda: specs)


@pytest.mark.db
@pytest.mark.regression("13757")
def test_buildcache_list_duplicates(mock_get_specs, capsys):
    with capsys.disabled():
        output = buildcache("list", "mpileaks", "@2.3")

    assert output.count("mpileaks") == 3


@pytest.mark.db
@pytest.mark.regression("17827")
def test_buildcache_list_allarch(database, mock_get_specs_multiarch, capsys):
    with capsys.disabled():
        output = buildcache("list", "--allarch")

    assert output.count("mpileaks") == 3

    with capsys.disabled():
        output = buildcache("list")

    assert output.count("mpileaks") == 2


def tests_buildcache_create(install_mockery, mock_fetch, monkeypatch, tmpdir):
    """ "Ensure that buildcache create creates output files"""
    pkg = "trivial-install-test-package"
    install(pkg)

    buildcache("push", "--unsigned", str(tmpdir), pkg)

    spec = Spec(pkg).concretized()
    tarball_path = spack.binary_distribution.tarball_path_name(spec, ".spack")
    tarball = spack.binary_distribution.tarball_name(spec, ".spec.json")
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball_path))
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball))


def tests_buildcache_create_env(
    install_mockery, mock_fetch, monkeypatch, tmpdir, mutable_mock_env_path
):
    """ "Ensure that buildcache create creates output files from env"""
    pkg = "trivial-install-test-package"

    env("create", "test")
    with ev.read("test"):
        add(pkg)
        install()

        buildcache("push", "--unsigned", str(tmpdir))

    spec = Spec(pkg).concretized()
    tarball_path = spack.binary_distribution.tarball_path_name(spec, ".spack")
    tarball = spack.binary_distribution.tarball_name(spec, ".spec.json")
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball_path))
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball))


def test_buildcache_create_fails_on_noargs(tmpdir):
    """Ensure that buildcache create fails when given no args or
    environment."""
    with pytest.raises(spack.main.SpackCommandError):
        buildcache("push", "--unsigned", str(tmpdir))


def test_buildcache_create_fail_on_perm_denied(install_mockery, mock_fetch, monkeypatch, tmpdir):
    """Ensure that buildcache create fails on permission denied error."""
    install("trivial-install-test-package")

    tmpdir.chmod(0)
    with pytest.raises(OSError) as error:
        buildcache("push", "--unsigned", str(tmpdir), "trivial-install-test-package")
    assert error.value.errno == errno.EACCES
    tmpdir.chmod(0o700)


def test_update_key_index(
    tmpdir,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    mock_fetch,
    mock_stage,
    mock_gnupghome,
):
    """Test the update-index command with the --keys option"""
    working_dir = tmpdir.join("working_dir")

    mirror_dir = working_dir.join("mirror")
    mirror_url = "file://{0}".format(mirror_dir.strpath)

    mirror("add", "test-mirror", mirror_url)

    gpg("create", "Test Signing Key", "nobody@nowhere.com")

    s = Spec("libdwarf").concretized()

    # Install a package
    install(s.name)

    # Put installed package in the buildcache, which, because we're signing
    # it, should result in the public key getting pushed to the buildcache
    # as well.
    buildcache("push", mirror_dir.strpath, s.name)

    # Now make sure that when we pass the "--keys" argument to update-index
    # it causes the index to get update.
    buildcache("update-index", "--keys", mirror_dir.strpath)

    key_dir_list = os.listdir(os.path.join(mirror_dir.strpath, "build_cache", "_pgp"))

    uninstall("-y", s.name)
    mirror("rm", "test-mirror")

    assert "index.json" in key_dir_list


def test_buildcache_autopush(tmp_path, install_mockery, mock_fetch):
    """Test buildcache with autopush"""
    mirror_dir = tmp_path / "mirror"
    mirror_autopush_dir = tmp_path / "mirror_autopush"

    mirror("add", "--unsigned", "mirror", mirror_dir.as_uri())
    mirror("add", "--autopush", "--unsigned", "mirror-autopush", mirror_autopush_dir.as_uri())

    s = Spec("libdwarf").concretized()

    # Install and generate build cache index
    PackageInstaller([s.package], explicit=True).install()

    metadata_file = spack.binary_distribution.tarball_name(s, ".spec.json")

    assert not (mirror_dir / "build_cache" / metadata_file).exists()
    assert (mirror_autopush_dir / "build_cache" / metadata_file).exists()


def test_buildcache_sync(
    mutable_mock_env_path, install_mockery, mock_packages, mock_fetch, mock_stage, tmpdir
):
    """
    Make sure buildcache sync works in an environment-aware manner, ignoring
    any specs that may be in the mirror but not in the environment.
    """
    working_dir = tmpdir.join("working_dir")

    src_mirror_dir = working_dir.join("src_mirror").strpath
    src_mirror_url = "file://{0}".format(src_mirror_dir)

    dest_mirror_dir = working_dir.join("dest_mirror").strpath
    dest_mirror_url = "file://{0}".format(dest_mirror_dir)

    in_env_pkg = "trivial-install-test-package"
    out_env_pkg = "libdwarf"

    def verify_mirror_contents():
        dest_list = os.listdir(os.path.join(dest_mirror_dir, "build_cache"))

        found_pkg = False

        for p in dest_list:
            assert out_env_pkg not in p
            if in_env_pkg in p:
                found_pkg = True

        if not found_pkg:
            print("Expected to find {0} in {1}".format(in_env_pkg, dest_mirror_dir))
            assert False

    # Install a package and put it in the buildcache
    s = Spec(out_env_pkg).concretized()
    install(s.name)
    buildcache("push", "-u", "-f", src_mirror_url, s.name)

    env("create", "test")
    with ev.read("test"):
        add(in_env_pkg)
        install()
        buildcache("push", "-u", "-f", src_mirror_url, in_env_pkg)

        # Now run the spack buildcache sync command with all the various options
        # for specifying mirrors

        # Use urls to specify mirrors
        buildcache("sync", src_mirror_url, dest_mirror_url)

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)

        # Use local directory paths to specify fs locations
        buildcache("sync", src_mirror_dir, dest_mirror_dir)

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)

        # Use mirror names to specify mirrors
        mirror("add", "src", src_mirror_url)
        mirror("add", "dest", dest_mirror_url)
        mirror("add", "ignored", "file:///dummy/io")

        buildcache("sync", "src", "dest")

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)

        def manifest_insert(manifest, spec, dest_url):
            manifest[spec.dag_hash()] = [
                {
                    "src": spack.util.url.join(
                        src_mirror_url,
                        spack.binary_distribution.build_cache_relative_path(),
                        spack.binary_distribution.tarball_name(spec, ".spec.json"),
                    ),
                    "dest": spack.util.url.join(
                        dest_url,
                        spack.binary_distribution.build_cache_relative_path(),
                        spack.binary_distribution.tarball_name(spec, ".spec.json"),
                    ),
                },
                {
                    "src": spack.util.url.join(
                        src_mirror_url,
                        spack.binary_distribution.build_cache_relative_path(),
                        spack.binary_distribution.tarball_path_name(spec, ".spack"),
                    ),
                    "dest": spack.util.url.join(
                        dest_url,
                        spack.binary_distribution.build_cache_relative_path(),
                        spack.binary_distribution.tarball_path_name(spec, ".spack"),
                    ),
                },
            ]

        manifest_file = os.path.join(tmpdir.strpath, "manifest_dest.json")
        with open(manifest_file, "w") as fd:
            test_env = ev.active_environment()

            manifest = {}
            for spec in test_env.specs_by_hash.values():
                manifest_insert(manifest, spec, dest_mirror_url)
            json.dump(manifest, fd)

        buildcache("sync", "--manifest-glob", manifest_file)

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)

        manifest_file = os.path.join(tmpdir.strpath, "manifest_bad_dest.json")
        with open(manifest_file, "w") as fd:
            manifest = {}
            for spec in test_env.specs_by_hash.values():
                manifest_insert(
                    manifest, spec, spack.util.url.join(dest_mirror_url, "invalid_path")
                )
            json.dump(manifest, fd)

        # Trigger the warning
        output = buildcache("sync", "--manifest-glob", manifest_file, "dest", "ignored")

        assert "Ignoring unused arguemnt: ignored" in output

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)


def test_buildcache_create_install(
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    mock_fetch,
    mock_stage,
    monkeypatch,
    tmpdir,
):
    """ "Ensure that buildcache create creates output files"""
    pkg = "trivial-install-test-package"
    install(pkg)

    buildcache("push", "--unsigned", str(tmpdir), pkg)

    spec = Spec(pkg).concretized()
    tarball_path = spack.binary_distribution.tarball_path_name(spec, ".spack")
    tarball = spack.binary_distribution.tarball_name(spec, ".spec.json")
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball_path))
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball))


@pytest.mark.parametrize(
    "things_to_install,expected",
    [
        (
            "",
            [
                "dttop",
                "dtbuild1",
                "dtbuild2",
                "dtlink2",
                "dtrun2",
                "dtlink1",
                "dtlink3",
                "dtlink4",
                "dtrun1",
                "dtlink5",
                "dtrun3",
                "dtbuild3",
            ],
        ),
        (
            "dependencies",
            [
                "dtbuild1",
                "dtbuild2",
                "dtlink2",
                "dtrun2",
                "dtlink1",
                "dtlink3",
                "dtlink4",
                "dtrun1",
                "dtlink5",
                "dtrun3",
                "dtbuild3",
            ],
        ),
        ("package", ["dttop"]),
    ],
)
def test_correct_specs_are_pushed(
    things_to_install, expected, tmpdir, monkeypatch, default_mock_concretization, temporary_store
):
    spec = default_mock_concretization("dttop")
    PackageInstaller([spec.package], explicit=True, fake=True).install()
    slash_hash = f"/{spec.dag_hash()}"

    class DontUpload(spack.binary_distribution.Uploader):
        def __init__(self):
            super().__init__(spack.mirror.Mirror.from_local_path(str(tmpdir)), False, False)
            self.pushed = []

        def push(self, specs: List[spack.spec.Spec]):
            self.pushed.extend(s.name for s in specs)
            return [], []  # nothing skipped, nothing errored

    uploader = DontUpload()

    monkeypatch.setattr(
        spack.binary_distribution, "make_uploader", lambda *args, **kwargs: uploader
    )

    buildcache_create_args = ["create", "--unsigned"]

    if things_to_install != "":
        buildcache_create_args.extend(["--only", things_to_install])

    buildcache_create_args.extend([str(tmpdir), slash_hash])

    buildcache(*buildcache_create_args)

    # Order is not guaranteed, so we can't just compare lists
    assert set(uploader.pushed) == set(expected)

    # Ensure no duplicates
    assert len(set(uploader.pushed)) == len(uploader.pushed)


@pytest.mark.parametrize("signed", [True, False])
def test_push_and_install_with_mirror_marked_unsigned_does_not_require_extra_flags(
    tmp_path, mutable_database, mock_gnupghome, signed
):
    """Tests whether marking a mirror as unsigned makes it possible to push and install to/from
    it without requiring extra flags on the command line (and no signing keys configured)."""

    # Create a named mirror with signed set to True or False
    add_flag = "--signed" if signed else "--unsigned"
    mirror("add", add_flag, "my-mirror", str(tmp_path))
    spec = mutable_database.query_local("libelf", installed=True)[0]

    # Push
    if signed:
        # Need to pass "--unsigned" to override the mirror's default
        args = ["push", "--update-index", "--unsigned", "my-mirror", f"/{spec.dag_hash()}"]
    else:
        # No need to pass "--unsigned" if the mirror is unsigned
        args = ["push", "--update-index", "my-mirror", f"/{spec.dag_hash()}"]

    buildcache(*args)

    # Install
    if signed:
        # Need to pass "--no-check-signature" to avoid install errors
        kwargs = {"explicit": True, "cache_only": True, "unsigned": True}
    else:
        # No need to pass "--no-check-signature" if the mirror is unsigned
        kwargs = {"explicit": True, "cache_only": True}

    spec.package.do_uninstall(force=True)
    PackageInstaller([spec.package], **kwargs).install()


def test_skip_no_redistribute(mock_packages, config):
    specs = list(Spec("no-redistribute-dependent").concretized().traverse())
    filtered = spack.cmd.buildcache._skip_no_redistribute_for_public(specs)
    assert not any(s.name == "no-redistribute" for s in filtered)
    assert any(s.name == "no-redistribute-dependent" for s in filtered)


def test_best_effort_vs_fail_fast_when_dep_not_installed(tmp_path, mutable_database):
    """When --fail-fast is passed, the push command should fail if it immediately finds an
    uninstalled dependency. Otherwise, failure to push one dependency shouldn't prevent the
    others from being pushed."""

    mirror("add", "--unsigned", "my-mirror", str(tmp_path))

    # Uninstall mpich so that its dependent mpileaks can't be pushed
    for s in mutable_database.query_local("mpich"):
        s.package.do_uninstall(force=True)

    with pytest.raises(spack.cmd.buildcache.PackagesAreNotInstalledError, match="mpich"):
        buildcache("push", "--update-index", "--fail-fast", "my-mirror", "mpileaks^mpich")

    # nothing should be pushed due to --fail-fast.
    assert not os.listdir(tmp_path)
    assert not spack.binary_distribution.update_cache_and_get_specs()

    with pytest.raises(spack.cmd.buildcache.PackageNotInstalledError):
        buildcache("push", "--update-index", "my-mirror", "mpileaks^mpich")

    specs = spack.binary_distribution.update_cache_and_get_specs()

    # everything but mpich should be pushed
    mpileaks = mutable_database.query_local("mpileaks^mpich")[0]
    assert set(specs) == {s for s in mpileaks.traverse() if s.name != "mpich"}


def test_push_without_build_deps(tmp_path, temporary_store, mock_packages, mutable_config):
    """Spack should not error when build deps are uninstalled and --without-build-dependenies is
    passed."""

    mirror("add", "--unsigned", "my-mirror", str(tmp_path))

    s = spack.spec.Spec("dtrun3").concretized()
    PackageInstaller([s.package], explicit=True, fake=True).install()
    s["dtbuild3"].package.do_uninstall()

    # fails when build deps are required
    with pytest.raises(spack.error.SpackError, match="package not installed"):
        buildcache(
            "push", "--update-index", "--with-build-dependencies", "my-mirror", f"/{s.dag_hash()}"
        )

    # succeeds when build deps are not required
    buildcache(
        "push", "--update-index", "--without-build-dependencies", "my-mirror", f"/{s.dag_hash()}"
    )
    assert spack.binary_distribution.update_cache_and_get_specs() == [s]
