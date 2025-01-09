# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import copy
import os
import shutil

import pytest

from llnl.util.filesystem import mkdirp, touch, working_dir

import spack.config
import spack.error
import spack.fetch_strategy
import spack.platforms
import spack.repo
from spack.fetch_strategy import GitFetchStrategy
from spack.spec import Spec
from spack.stage import Stage
from spack.version import Version

_mock_transport_error = "Mock HTTP transport error"


@pytest.fixture(params=[None, "1.8.5.2", "1.8.5.1", "1.7.10", "1.7.1", "1.7.0"])
def git_version(git, request, monkeypatch):
    """Tests GitFetchStrategy behavior for different git versions.

    GitFetchStrategy tries to optimize using features of newer git
    versions, but needs to work with older git versions.  To ensure code
    paths for old versions still work, we fake it out here and make it
    use the backward-compatibility code paths with newer git versions.
    """
    real_git_version = spack.fetch_strategy.GitFetchStrategy.version_from_git(git)

    if request.param is None:
        # Don't patch; run with the real git_version method.
        yield real_git_version
    else:
        test_git_version = Version(request.param)
        if test_git_version > real_git_version:
            pytest.skip("Can't test clone logic for newer version of git.")

        # Patch the fetch strategy to think it's using a lower git version.
        # we use this to test what we'd need to do with older git versions
        # using a newer git installation.
        monkeypatch.setattr(GitFetchStrategy, "git_version", test_git_version)
        yield test_git_version


@pytest.fixture
def mock_bad_git(monkeypatch):
    """
    Test GitFetchStrategy behavior with a bad git command for git >= 1.7.1
    to trigger a SpackError.
    """

    def bad_git(*args, **kwargs):
        """Raise a SpackError with the transport message."""
        raise spack.error.SpackError(_mock_transport_error)

    # Patch the fetch strategy to think it's using a git version that
    # will error out when git is called.
    monkeypatch.setattr(GitFetchStrategy, "git", bad_git)
    monkeypatch.setattr(GitFetchStrategy, "git_version", Version("1.7.1"))
    yield


def test_bad_git(tmpdir, mock_bad_git):
    """Trigger a SpackError when attempt a fetch with a bad git."""
    testpath = str(tmpdir)

    with pytest.raises(spack.error.SpackError):
        fetcher = GitFetchStrategy(git="file:///not-a-real-git-repo")
        with Stage(fetcher, path=testpath):
            fetcher.fetch()


@pytest.mark.parametrize("type_of_test", ["default", "branch", "tag", "commit"])
@pytest.mark.parametrize("secure", [True, False])
def test_fetch(
    git,
    type_of_test,
    secure,
    mock_git_repository,
    default_mock_concretization,
    mutable_mock_repo,
    git_version,
    monkeypatch,
):
    """Tries to:

    1. Fetch the repo using a fetch strategy constructed with
       supplied args (they depend on type_of_test).
    2. Check if the test_file is in the checked out repository.
    3. Assert that the repository is at the revision supplied.
    4. Add and remove some files, then reset the repo, and
       ensure it's all there again.
    """
    # Retrieve the right test parameters
    t = mock_git_repository.checks[type_of_test]
    h = mock_git_repository.hash

    pkg_class = spack.repo.PATH.get_pkg_class("git-test")
    # This would fail using the default-no-per-version-git check but that
    # isn't included in this test
    monkeypatch.delattr(pkg_class, "git")

    # Construct the package under test
    s = default_mock_concretization("git-test")
    monkeypatch.setitem(s.package.versions, Version("git"), t.args)

    # Enter the stage directory and check some properties
    with s.package.stage:
        with spack.config.override("config:verify_ssl", secure):
            s.package.do_stage()

        with working_dir(s.package.stage.source_path):
            assert h("HEAD") == h(t.revision)

            file_path = os.path.join(s.package.stage.source_path, t.file)
            assert os.path.isdir(s.package.stage.source_path)
            assert os.path.isfile(file_path)

            os.unlink(file_path)
            assert not os.path.isfile(file_path)

            untracked_file = "foobarbaz"
            touch(untracked_file)
            assert os.path.isfile(untracked_file)
            s.package.do_restage()
            assert not os.path.isfile(untracked_file)

            assert os.path.isdir(s.package.stage.source_path)
            assert os.path.isfile(file_path)

            assert h("HEAD") == h(t.revision)


@pytest.mark.disable_clean_stage_check
def test_fetch_pkg_attr_submodule_init(
    mock_git_repository, default_mock_concretization, mutable_mock_repo, monkeypatch, mock_stage
):
    """In this case the version() args do not contain a 'git' URL, so
    the fetcher must be assembled using the Package-level 'git' attribute.
    This test ensures that the submodules are properly initialized and the
    expected branch file is present.
    """

    t = mock_git_repository.checks["default-no-per-version-git"]
    pkg_class = spack.repo.PATH.get_pkg_class("git-test")
    # For this test, the version args don't specify 'git' (which is
    # the majority of version specifications)
    monkeypatch.setattr(pkg_class, "git", mock_git_repository.url)

    # Construct the package under test
    s = default_mock_concretization("git-test")
    monkeypatch.setitem(s.package.versions, Version("git"), t.args)

    s.package.do_stage()
    collected_fnames = set()
    for root, dirs, files in os.walk(s.package.stage.source_path):
        collected_fnames.update(files)
    # The submodules generate files with the prefix "r0_file_"
    assert {"r0_file_0", "r0_file_1", t.file} < collected_fnames


@pytest.mark.skipif(
    str(spack.platforms.host()) == "windows",
    reason=(
        "Git fails to clone because the src/dst paths"
        " are too long: the name of the staging directory"
        " for ad-hoc Git commit versions is longer than"
        " other staged sources"
    ),
)
@pytest.mark.disable_clean_stage_check
def test_adhoc_version_submodules(
    mock_git_repository, config, mutable_mock_repo, monkeypatch, mock_stage
):
    t = mock_git_repository.checks["tag"]
    # Construct the package under test
    pkg_class = spack.repo.PATH.get_pkg_class("git-test")
    monkeypatch.setitem(pkg_class.versions, Version("git"), t.args)
    monkeypatch.setattr(pkg_class, "git", "file://%s" % mock_git_repository.path, raising=False)

    spec = Spec("git-test@{0}".format(mock_git_repository.unversioned_commit))
    spec.concretize()
    spec.package.do_stage()
    collected_fnames = set()
    for root, dirs, files in os.walk(spec.package.stage.source_path):
        collected_fnames.update(files)
    # The submodules generate files with the prefix "r0_file_"
    assert set(["r0_file_0", "r0_file_1"]) < collected_fnames


@pytest.mark.parametrize("type_of_test", ["branch", "commit"])
def test_debug_fetch(
    mock_packages, type_of_test, mock_git_repository, default_mock_concretization, monkeypatch
):
    """Fetch the repo with debug enabled."""
    # Retrieve the right test parameters
    t = mock_git_repository.checks[type_of_test]

    # Construct the package under test
    s = default_mock_concretization("git-test")
    monkeypatch.setitem(s.package.versions, Version("git"), t.args)

    # Fetch then ensure source path exists
    with s.package.stage:
        with spack.config.override("config:debug", True):
            s.package.do_fetch()
            assert os.path.isdir(s.package.stage.source_path)


def test_git_extra_fetch(git, tmpdir):
    """Ensure a fetch after 'expanding' is effectively a no-op."""
    testpath = str(tmpdir)

    fetcher = GitFetchStrategy(git="file:///not-a-real-git-repo")
    with Stage(fetcher, path=testpath) as stage:
        mkdirp(stage.source_path)
        fetcher.fetch()  # Use fetcher to fetch for code coverage
        shutil.rmtree(stage.source_path)


def test_needs_stage(git):
    """Trigger a NoStageError when attempt a fetch without a stage."""
    with pytest.raises(
        spack.fetch_strategy.NoStageError, match=r"set_stage.*before calling fetch"
    ):
        fetcher = GitFetchStrategy(git="file:///not-a-real-git-repo")
        fetcher.fetch()


@pytest.mark.parametrize("get_full_repo", [True, False])
def test_get_full_repo(
    get_full_repo,
    git_version,
    mock_git_repository,
    default_mock_concretization,
    mutable_mock_repo,
    monkeypatch,
):
    """Ensure that we can clone a full repository."""

    if git_version < Version("1.7.1"):
        pytest.skip("Not testing get_full_repo for older git {0}".format(git_version))

    secure = True
    type_of_test = "tag-branch"

    t = mock_git_repository.checks[type_of_test]

    s = default_mock_concretization("git-test")
    args = copy.copy(t.args)
    args["get_full_repo"] = get_full_repo
    monkeypatch.setitem(s.package.versions, Version("git"), args)

    with s.package.stage:
        with spack.config.override("config:verify_ssl", secure):
            s.package.do_stage()
            with working_dir(s.package.stage.source_path):
                branches = mock_git_repository.git_exe("branch", "-a", output=str).splitlines()
                nbranches = len(branches)
                commits = mock_git_repository.git_exe(
                    "log",
                    "--graph",
                    "--pretty=format:%h -%d %s (%ci) <%an>",
                    "--abbrev-commit",
                    output=str,
                ).splitlines()
                ncommits = len(commits)

        if get_full_repo:
            assert nbranches >= 5
            assert ncommits == 2
        else:
            assert nbranches == 2
            assert ncommits == 1


@pytest.mark.disable_clean_stage_check
@pytest.mark.parametrize("submodules", [True, False])
def test_gitsubmodule(
    submodules, mock_git_repository, default_mock_concretization, mutable_mock_repo, monkeypatch
):
    """
    Test GitFetchStrategy behavior with submodules. This package
    has a `submodules` property which is always True: when a specific
    version also indicates to include submodules, this should not
    interfere; if the specific version explicitly requests that
    submodules *not* be initialized, this should override the
    Package-level request.
    """
    type_of_test = "tag-branch"
    t = mock_git_repository.checks[type_of_test]

    # Construct the package under test
    s = default_mock_concretization("git-test")
    args = copy.copy(t.args)
    args["submodules"] = submodules
    monkeypatch.setitem(s.package.versions, Version("git"), args)
    s.package.do_stage()
    with working_dir(s.package.stage.source_path):
        for submodule_count in range(2):
            file_path = os.path.join(
                s.package.stage.source_path,
                "third_party/submodule{0}/r0_file_{0}".format(submodule_count),
            )
            if submodules:
                assert os.path.isfile(file_path)
            else:
                assert not os.path.isfile(file_path)


@pytest.mark.disable_clean_stage_check
def test_gitsubmodules_callable(
    mock_git_repository, default_mock_concretization, mutable_mock_repo, monkeypatch
):
    """
    Test GitFetchStrategy behavior with submodules selected after concretization
    """

    def submodules_callback(package):
        name = "third_party/submodule0"
        return [name]

    type_of_test = "tag-branch"
    t = mock_git_repository.checks[type_of_test]

    # Construct the package under test
    s = default_mock_concretization("git-test")
    args = copy.copy(t.args)
    args["submodules"] = submodules_callback
    monkeypatch.setitem(s.package.versions, Version("git"), args)
    s.package.do_stage()
    with working_dir(s.package.stage.source_path):
        file_path = os.path.join(s.package.stage.source_path, "third_party/submodule0/r0_file_0")
        assert os.path.isfile(file_path)
        file_path = os.path.join(s.package.stage.source_path, "third_party/submodule1/r0_file_1")
        assert not os.path.isfile(file_path)


@pytest.mark.disable_clean_stage_check
def test_gitsubmodules_delete(
    mock_git_repository, default_mock_concretization, mutable_mock_repo, monkeypatch
):
    """
    Test GitFetchStrategy behavior with submodules_delete
    """
    type_of_test = "tag-branch"
    t = mock_git_repository.checks[type_of_test]

    # Construct the package under test
    s = default_mock_concretization("git-test")
    args = copy.copy(t.args)
    args["submodules"] = True
    args["submodules_delete"] = ["third_party/submodule0", "third_party/submodule1"]
    monkeypatch.setitem(s.package.versions, Version("git"), args)
    s.package.do_stage()
    with working_dir(s.package.stage.source_path):
        file_path = os.path.join(s.package.stage.source_path, "third_party/submodule0")
        assert not os.path.isdir(file_path)
        file_path = os.path.join(s.package.stage.source_path, "third_party/submodule1")
        assert not os.path.isdir(file_path)


@pytest.mark.disable_clean_stage_check
def test_gitsubmodules_falsey(
    mock_git_repository, default_mock_concretization, mutable_mock_repo, monkeypatch
):
    """
    Test GitFetchStrategy behavior when callable submodules returns Falsey
    """

    def submodules_callback(package):
        return False

    type_of_test = "tag-branch"
    t = mock_git_repository.checks[type_of_test]

    # Construct the package under test
    s = default_mock_concretization("git-test")
    args = copy.copy(t.args)
    args["submodules"] = submodules_callback
    monkeypatch.setitem(s.package.versions, Version("git"), args)
    s.package.do_stage()
    with working_dir(s.package.stage.source_path):
        file_path = os.path.join(s.package.stage.source_path, "third_party/submodule0/r0_file_0")
        assert not os.path.isfile(file_path)
        file_path = os.path.join(s.package.stage.source_path, "third_party/submodule1/r0_file_1")
        assert not os.path.isfile(file_path)


@pytest.mark.disable_clean_stage_check
def test_git_sparse_paths_partial_clone(
    mock_git_repository, git_version, default_mock_concretization, mutable_mock_repo, monkeypatch
):
    """
    Test partial clone of repository when using git_sparse_paths property
    """
    type_of_test = "many-directories"
    sparse_paths = ["dir0"]
    omitted_paths = ["dir1", "dir2"]
    t = mock_git_repository.checks[type_of_test]
    args = copy.copy(t.args)
    args["git_sparse_paths"] = sparse_paths
    s = default_mock_concretization("git-test")
    monkeypatch.setitem(s.package.versions, Version("git"), args)
    s.package.do_stage()
    with working_dir(s.package.stage.source_path):
        # top level directory files are cloned via sparse-checkout
        assert os.path.isfile("r0_file")

        for p in sparse_paths:
            assert os.path.isdir(p)

        if git_version < Version("2.26.0.0"):
            # older versions of git should fall back to a full clone
            for p in omitted_paths:
                assert os.path.isdir(p)
        else:
            for p in omitted_paths:
                assert not os.path.isdir(p)

        # fixture file is in the sparse-path expansion tree
        assert os.path.isfile(t.file)
