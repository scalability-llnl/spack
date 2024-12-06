# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

import pytest

import llnl.util.filesystem as fs

import spack.config
import spack.environment as ev
import spack.package_base
import spack.spec
import spack.stage
import spack.util.git
import spack.util.path
from spack.main import SpackCommand

add = SpackCommand("add")
develop = SpackCommand("develop")
env = SpackCommand("env")


@pytest.mark.usefixtures("mutable_mock_env_path", "mock_packages", "mock_fetch", "mutable_config")
class TestDevelop:
    def check_develop(self, env, spec, path=None, build_dir=None):
        path = path or spec.name

        # check in memory representation
        assert spec.name in env.dev_specs
        dev_specs_entry = env.dev_specs[spec.name]
        assert dev_specs_entry["path"] == path
        assert dev_specs_entry["spec"] == str(spec)

        # check yaml representation
        dev_config = spack.config.get("develop", {})
        assert spec.name in dev_config
        yaml_entry = dev_config[spec.name]
        assert yaml_entry["spec"] == str(spec)
        if path == spec.name:
            # default paths aren't written out
            assert "path" not in yaml_entry
        else:
            assert yaml_entry["path"] == path

        if build_dir is not None:
            scope = env.scope_name
            assert build_dir == spack.config.get(
                "packages:{}:package_attributes:build_directory".format(spec.name), scope
            )

    def test_develop_no_path_no_clone(self):
        env("create", "test")
        with ev.read("test") as e:
            # develop checks that the path exists
            fs.mkdirp(os.path.join(e.path, "mpich"))
            develop("--no-clone", "mpich@1.0")
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"))

    def test_develop_no_clone(self, tmpdir):
        env("create", "test")
        with ev.read("test") as e:
            develop("--no-clone", "-p", str(tmpdir), "mpich@1.0")
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"), str(tmpdir))

    def test_develop_no_version(self, tmpdir):
        env("create", "test")
        with ev.read("test") as e:
            develop("--no-clone", "-p", str(tmpdir), "mpich")
            self.check_develop(e, spack.spec.Spec("mpich@=main"), str(tmpdir))

    def test_develop(self):
        env("create", "test")
        with ev.read("test") as e:
            develop("mpich@1.0")
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"))

    def test_develop_no_args(self):
        env("create", "test")
        with ev.read("test") as e:
            # develop and remove it
            develop("mpich@1.0")
            shutil.rmtree(os.path.join(e.path, "mpich"))

            # test develop with no args
            develop()
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"))

    def test_develop_build_directory(self):
        env("create", "test")
        with ev.read("test") as e:
            develop("-b", "test_build_dir", "mpich@1.0")
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"), None, "test_build_dir")

    def test_develop_twice(self):
        env("create", "test")
        with ev.read("test") as e:
            develop("mpich@1.0")
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"))

            develop("mpich@1.0")
            # disk representation isn't updated unless we write
            # second develop command doesn't change it, so we don't write
            # but we check disk representation
            e.write()
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"))
            assert len(e.dev_specs) == 1

    def test_develop_update_path(self, tmpdir):
        env("create", "test")
        with ev.read("test") as e:
            develop("mpich@1.0")
            develop("-p", str(tmpdir), "mpich@1.0")
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"), str(tmpdir))
            assert len(e.dev_specs) == 1

    def test_develop_update_spec(self):
        env("create", "test")
        with ev.read("test") as e:
            develop("mpich@1.0")
            develop("mpich@2.0")
            self.check_develop(e, spack.spec.Spec("mpich@=2.0"))
            assert len(e.dev_specs) == 1

    def test_develop_canonicalize_path(self, monkeypatch):
        env("create", "test")
        with ev.read("test") as e:
            path = "../$user"
            abspath = spack.util.path.canonicalize_path(path, e.path)

            def check_path(stage, dest):
                assert dest == abspath

            monkeypatch.setattr(spack.stage.Stage, "steal_source", check_path)

            develop("-p", path, "mpich@1.0")
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"), path)

            # Check modifications actually worked
            assert spack.spec.Spec("mpich@1.0").concretized().satisfies("dev_path=%s" % abspath)

    def test_develop_canonicalize_path_no_args(self, monkeypatch):
        env("create", "test")
        with ev.read("test") as e:
            path = "$user"
            abspath = spack.util.path.canonicalize_path(path, e.path)

            def check_path(stage, dest):
                assert dest == abspath

            monkeypatch.setattr(spack.stage.Stage, "steal_source", check_path)

            # Defensive check to ensure canonicalization failures don't pollute FS
            assert abspath.startswith(e.path)

            # Create path to allow develop to modify env
            fs.mkdirp(abspath)
            develop("--no-clone", "-p", path, "mpich@1.0")

            # Remove path to ensure develop with no args runs staging code
            os.rmdir(abspath)

            develop()
            self.check_develop(e, spack.spec.Spec("mpich@=1.0"), path)

            # Check modifications actually worked
            assert spack.spec.Spec("mpich@1.0").concretized().satisfies("dev_path=%s" % abspath)


def _git_commit_list(git_repo_dir):
    git = spack.util.git.git()
    with fs.working_dir(git_repo_dir):
        output = git("log", "--pretty=format:%h", "-n", "20", output=str)
    return output.strip().split()


def test_develop_full_git_repo(
    mutable_mock_env_path,
    mock_git_version_info,
    install_mockery,
    mock_packages,
    monkeypatch,
    tmpdir,
    mutable_config,
    request,
):
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", "file://%s" % repo_path, raising=False
    )

    spec = spack.spec.Spec("git-test-commit@1.2").concretized()
    try:
        spec.package.do_stage()
        commits = _git_commit_list(spec.package.stage[0].source_path)
        # Outside of "spack develop" Spack will only pull exactly the commit it
        # needs, with no additional history
        assert len(commits) == 1
    finally:
        spec.package.do_clean()

    # Now use "spack develop": look at the resulting dev_path and make
    # sure the git repo pulled includes the full branch history (or rather,
    # more than just one commit).
    env("create", "test")
    with ev.read("test") as e:
        add("git-test-commit")
        develop("git-test-commit@1.2")

        e.concretize()
        spec = e.all_specs()[0]
        develop_dir = spec.variants["dev_path"].value
        commits = _git_commit_list(develop_dir)
        assert len(commits) > 1
