# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import llnl.util.filesystem as fs

import spack.environment as ev
import spack.error
import spack.repo
import spack.spec
import spack.store
from spack.main import SpackCommand

dev_build = SpackCommand("dev-build")
install = SpackCommand("install")
env = SpackCommand("env")

pytestmark = [pytest.mark.disable_clean_stage_check]


def test_dev_build_basics(tmpdir, install_mockery):
    spec = spack.spec.Spec(f"dev-build-test-install@0.0.0 dev_path={tmpdir}").concretized()

    assert "dev_path" in spec.variants

    with tmpdir.as_cwd():
        with open(spec.package.filename, "w") as f:
            f.write(spec.package.original_string)

        dev_build("dev-build-test-install@0.0.0")

    assert spec.package.filename in os.listdir(spec.prefix)
    with open(os.path.join(spec.prefix, spec.package.filename), "r") as f:
        assert f.read() == spec.package.replacement_string

    assert os.path.exists(str(tmpdir))


def test_dev_build_before(tmpdir, install_mockery):
    spec = spack.spec.Spec(f"dev-build-test-install@0.0.0 dev_path={tmpdir}").concretized()

    with tmpdir.as_cwd():
        with open(spec.package.filename, "w") as f:
            f.write(spec.package.original_string)

        dev_build("-b", "edit", "dev-build-test-install@0.0.0")

        assert spec.package.filename in os.listdir(os.getcwd())
        with open(spec.package.filename, "r") as f:
            assert f.read() == spec.package.original_string

    assert not os.path.exists(spec.prefix)


def test_dev_build_until(tmpdir, install_mockery):
    spec = spack.spec.Spec(f"dev-build-test-install@0.0.0 dev_path={tmpdir}").concretized()

    with tmpdir.as_cwd():
        with open(spec.package.filename, "w") as f:
            f.write(spec.package.original_string)

        dev_build("-u", "edit", "dev-build-test-install@0.0.0")

        assert spec.package.filename in os.listdir(os.getcwd())
        with open(spec.package.filename, "r") as f:
            assert f.read() == spec.package.replacement_string

    assert not os.path.exists(spec.prefix)
    assert not spack.store.STORE.db.query(spec, installed=True)


def test_dev_build_until_last_phase(tmpdir, install_mockery):
    # Test that we ignore the last_phase argument if it is already last
    spec = spack.spec.Spec(f"dev-build-test-install@0.0.0 dev_path={tmpdir}").concretized()

    with tmpdir.as_cwd():
        with open(spec.package.filename, "w") as f:
            f.write(spec.package.original_string)

        dev_build("-u", "install", "dev-build-test-install@0.0.0")

        assert spec.package.filename in os.listdir(os.getcwd())
        with open(spec.package.filename, "r") as f:
            assert f.read() == spec.package.replacement_string

    assert os.path.exists(spec.prefix)
    assert spack.store.STORE.db.query(spec, installed=True)
    assert os.path.exists(str(tmpdir))


def test_dev_build_before_until(tmpdir, install_mockery):
    spec = spack.spec.Spec(f"dev-build-test-install@0.0.0 dev_path={tmpdir}").concretized()

    with tmpdir.as_cwd():
        with open(spec.package.filename, "w") as f:
            f.write(spec.package.original_string)

        with pytest.raises(SystemExit):
            dev_build("-u", "edit", "-b", "edit", "dev-build-test-install@0.0.0")

        bad_phase = "phase_that_does_not_exist"
        not_allowed = "is not a valid phase"
        not_installed = "was not installed"
        out = dev_build("-u", bad_phase, "dev-build-test-install@0.0.0", fail_on_error=False)
        assert bad_phase in out
        assert not_allowed in out
        assert not_installed in out

        out = dev_build("-b", bad_phase, "dev-build-test-install@0.0.0", fail_on_error=False)
        assert bad_phase in out
        assert not_allowed in out
        assert not_installed in out


def print_spack_cc(*args):
    # Eat arguments and print environment variable to test
    print(os.environ.get("CC", ""))


def test_dev_build_drop_in(tmpdir, mock_packages, monkeypatch, install_mockery, working_env):
    monkeypatch.setattr(os, "execvp", print_spack_cc)
    with tmpdir.as_cwd():
        output = dev_build("-b", "edit", "--drop-in", "sh", "dev-build-test-install@0.0.0")
        assert os.path.join("lib", "spack", "env") in output


def test_dev_build_fails_already_installed(tmpdir, install_mockery):
    spec = spack.spec.Spec("dev-build-test-install@0.0.0 dev_path=%s" % tmpdir)
    spec.concretize()

    with tmpdir.as_cwd():
        with open(spec.package.filename, "w") as f:
            f.write(spec.package.original_string)

        dev_build("dev-build-test-install@0.0.0")
        output = dev_build("dev-build-test-install@0.0.0", fail_on_error=False)
        assert "Already installed in %s" % spec.prefix in output


def test_dev_build_fails_no_spec():
    output = dev_build(fail_on_error=False)
    assert "requires a package spec argument" in output


def test_dev_build_fails_multiple_specs(mock_packages):
    output = dev_build("libelf", "libdwarf", fail_on_error=False)
    assert "only takes one spec" in output


def test_dev_build_fails_nonexistent_package_name(mock_packages):
    output = ""

    try:
        dev_build("no_such_package")
        assert False, "no exception was raised!"
    except spack.repo.UnknownPackageError as e:
        output = e.message

    assert "Package 'no_such_package' not found" in output


def test_dev_build_fails_no_version(mock_packages):
    output = dev_build("dev-build-test-install", fail_on_error=False)
    assert "dev-build spec must have a single, concrete version" in output


def test_dev_build_env(tmpdir, install_mockery, mutable_mock_env_path):
    """Test Spack does dev builds for packages in develop section of env."""
    # setup dev-build-test-install package for dev build
    build_dir = tmpdir.mkdir("build")
    spec = spack.spec.Spec("dev-build-test-install@0.0.0 dev_path=%s" % build_dir)
    spec.concretize()

    with build_dir.as_cwd():
        with open(spec.package.filename, "w") as f:
            f.write(spec.package.original_string)

    # setup environment
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w") as f:
            f.write(
                f"""\
spack:
  specs:
  - dev-build-test-install@0.0.0

  develop:
    dev-build-test-install:
      spec: dev-build-test-install@0.0.0
      path: {os.path.relpath(str(build_dir), start=str(envdir))}
"""
            )
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

    assert spec.package.filename in os.listdir(spec.prefix)
    with open(os.path.join(spec.prefix, spec.package.filename), "r") as f:
        assert f.read() == spec.package.replacement_string


def test_dev_build_env_with_vars(tmpdir, install_mockery, mutable_mock_env_path, monkeypatch):
    """Test Spack does dev builds for packages in develop section of env (path with variables)."""
    # setup dev-build-test-install package for dev build
    build_dir = tmpdir.mkdir("build")
    spec = spack.spec.Spec(f"dev-build-test-install@0.0.0 dev_path={build_dir}")
    spec.concretize()

    # store the build path in an environment variable that will be used in the environment
    monkeypatch.setenv("CUSTOM_BUILD_PATH", build_dir)

    with build_dir.as_cwd(), open(spec.package.filename, "w") as f:
        f.write(spec.package.original_string)

    # setup environment
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w") as f:
            f.write(
                """\
spack:
  specs:
  - dev-build-test-install@0.0.0

  develop:
    dev-build-test-install:
      spec: dev-build-test-install@0.0.0
      path: $CUSTOM_BUILD_PATH
"""
            )
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

    assert spec.package.filename in os.listdir(spec.prefix)
    with open(os.path.join(spec.prefix, spec.package.filename), "r") as f:
        assert f.read() == spec.package.replacement_string


def test_dev_build_env_version_mismatch(tmpdir, install_mockery, mutable_mock_env_path):
    """Test Spack constraints concretization by develop specs."""
    # setup dev-build-test-install package for dev build
    build_dir = tmpdir.mkdir("build")
    spec = spack.spec.Spec("dev-build-test-install@0.0.0 dev_path=%s" % tmpdir)
    spec.concretize()

    with build_dir.as_cwd():
        with open(spec.package.filename, "w") as f:
            f.write(spec.package.original_string)

    # setup environment
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w") as f:
            f.write(
                f"""\
spack:
  specs:
  - dev-build-test-install@0.0.0

  develop:
    dev-build-test-install:
      spec: dev-build-test-install@1.1.1
      path: {build_dir}
"""
            )

        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            with pytest.raises((RuntimeError, spack.error.UnsatisfiableSpecError)):
                install()


def test_dev_build_multiple(tmpdir, install_mockery, mutable_mock_env_path, mock_fetch):
    """Test spack install with multiple developer builds

    Test that only the root needs to be specified in the environment
    Test that versions known only from the dev specs are included in the solve,
    even if they come from a non-root
    """
    # setup dev-build-test-install package for dev build
    # Wait to concretize inside the environment to set dev_path on the specs;
    # without the environment, the user would need to set dev_path for both the
    # root and dependency if they wanted a dev build for both.
    leaf_dir = tmpdir.mkdir("leaf")
    leaf_spec = spack.spec.Spec("dev-build-test-install@=1.0.0")  # non-existing version
    leaf_pkg_cls = spack.repo.PATH.get_pkg_class(leaf_spec.name)
    with leaf_dir.as_cwd():
        with open(leaf_pkg_cls.filename, "w") as f:
            f.write(leaf_pkg_cls.original_string)

    # setup dev-build-test-dependent package for dev build
    # don't concretize outside environment -- dev info will be wrong
    root_dir = tmpdir.mkdir("root")
    root_spec = spack.spec.Spec("dev-build-test-dependent@0.0.0")
    root_pkg_cls = spack.repo.PATH.get_pkg_class(root_spec.name)
    with root_dir.as_cwd():
        with open(root_pkg_cls.filename, "w") as f:
            f.write(root_pkg_cls.original_string)

    # setup environment
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w") as f:
            f.write(
                f"""\
spack:
  specs:
  - dev-build-test-dependent@0.0.0

  develop:
    dev-build-test-install:
      path: {leaf_dir}
      spec: dev-build-test-install@=1.0.0
    dev-build-test-dependent:
      spec: dev-build-test-dependent@0.0.0
      path: {root_dir}
"""
            )

        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            # Do concretization inside environment for dev info
            # These specs are the source of truth to compare against the installs
            leaf_spec.concretize()
            root_spec.concretize()

            # Do install
            install()

    for spec in (leaf_spec, root_spec):
        assert spec.package.filename in os.listdir(spec.prefix)
        with open(os.path.join(spec.prefix, spec.package.filename), "r") as f:
            assert f.read() == spec.package.replacement_string


def test_dev_build_env_dependency(tmpdir, install_mockery, mock_fetch, mutable_mock_env_path):
    """
    Test non-root specs in an environment are properly marked for dev builds.
    """
    # setup dev-build-test-install package for dev build
    build_dir = tmpdir.mkdir("build")
    spec = spack.spec.Spec("dependent-of-dev-build@0.0.0")
    dep_spec = spack.spec.Spec("dev-build-test-install")

    with build_dir.as_cwd():
        dep_pkg_cls = spack.repo.PATH.get_pkg_class(dep_spec.name)
        with open(dep_pkg_cls.filename, "w") as f:
            f.write(dep_pkg_cls.original_string)

    # setup environment
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w") as f:
            f.write(
                f"""\
spack:
  specs:
  - dependent-of-dev-build@0.0.0

  develop:
    dev-build-test-install:
      spec: dev-build-test-install@0.0.0
      path: {os.path.relpath(str(build_dir), start=str(envdir))}
"""
            )
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            # concretize in the environment to get the dev build info
            # equivalent to setting dev_build and dev_path variants
            # on all specs above
            spec.concretize()
            dep_spec.concretize()
            install()

    # Ensure that both specs installed properly
    assert dep_spec.package.filename in os.listdir(dep_spec.prefix)
    assert os.path.exists(spec.prefix)

    # Ensure variants set properly; ensure build_dir is absolute and normalized
    for dep in (dep_spec, spec["dev-build-test-install"]):
        assert dep.satisfies("dev_path=%s" % build_dir)
    assert spec.satisfies("^dev_path=*")


@pytest.mark.parametrize("test_spec", ["dev-build-test-install", "dependent-of-dev-build"])
def test_dev_build_rebuild_on_source_changes(
    test_spec, tmpdir, install_mockery, mutable_mock_env_path, mock_fetch
):
    """Test dev builds rebuild on changes to source code.

    ``test_spec = dev-build-test-install`` tests rebuild for changes to package
    ``test_spec = dependent-of-dev-build`` tests rebuild for changes to dep
    """
    # setup dev-build-test-install package for dev build
    build_dir = tmpdir.mkdir("build")
    spec = spack.spec.Spec("dev-build-test-install@0.0.0 dev_path=%s" % build_dir)
    spec.concretize()

    def reset_string():
        with build_dir.as_cwd():
            with open(spec.package.filename, "w") as f:
                f.write(spec.package.original_string)

    reset_string()

    # setup environment
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w") as f:
            f.write(
                f"""\
spack:
  specs:
  - {test_spec}@0.0.0

  develop:
    dev-build-test-install:
      spec: dev-build-test-install@0.0.0
      path: {build_dir}
"""
            )

        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

            reset_string()  # so the package will accept rebuilds

            fs.touch(os.path.join(str(build_dir), "test"))
            output = install()

    assert f"Installing {test_spec}" in output
