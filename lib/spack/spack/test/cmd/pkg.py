# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import shutil

import pytest

from llnl.util.filesystem import mkdirp, working_dir

import spack.cmd.pkg
import spack.main
import spack.paths
import spack.repo
import spack.util.file_cache

#: new fake package template
pkg_template = """\
from spack.package import *

class {name}(Package):
    homepage = "http://www.example.com"
    url      = "http://www.example.com/test-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        pass
"""

abc = {"mockpkg-a", "mockpkg-b", "mockpkg-c"}
abd = {"mockpkg-a", "mockpkg-b", "mockpkg-d"}


# Force all tests to use a git repository *in* the mock packages repo.
@pytest.fixture(scope="module")
def mock_pkg_git_repo(git, tmp_path_factory):
    """Copy the builtin.mock repo and make a mutable git repo inside it."""
    root_dir = tmp_path_factory.mktemp("mock_pkg_git_repo")
    repo_dir = root_dir / "builtin.mock"
    shutil.copytree(spack.paths.mock_packages_path, str(repo_dir))

    repo_cache = spack.util.file_cache.FileCache(str(root_dir / "cache"))
    mock_repo = spack.repo.RepoPath(str(repo_dir), cache=repo_cache)
    mock_repo_packages = mock_repo.repos[0].packages_path

    with working_dir(mock_repo_packages):
        git("init")

        # initial commit with mock packages
        # the -f is necessary in case people ignore build-* in their ignores
        git("add", "-f", ".")
        git("config", "user.email", "testing@spack.io")
        git("config", "user.name", "Spack Testing")
        git("-c", "commit.gpgsign=false", "commit", "-m", "initial mock repo commit")

        # add commit with mockpkg-a, mockpkg-b, mockpkg-c packages
        mkdirp("mockpkg-a", "mockpkg-b", "mockpkg-c")
        with open("mockpkg-a/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgA"))
        with open("mockpkg-b/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgB"))
        with open("mockpkg-c/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgC"))
        git("add", "mockpkg-a", "mockpkg-b", "mockpkg-c")
        git("-c", "commit.gpgsign=false", "commit", "-m", "add mockpkg-a, mockpkg-b, mockpkg-c")

        # remove mockpkg-c, add mockpkg-d
        with open("mockpkg-b/package.py", "a") as f:
            f.write("\n# change mockpkg-b")
        git("add", "mockpkg-b")
        mkdirp("mockpkg-d")
        with open("mockpkg-d/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgD"))
        git("add", "mockpkg-d")
        git("rm", "-rf", "mockpkg-c")
        git(
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-m",
            "change mockpkg-b, remove mockpkg-c, add mockpkg-d",
        )

    with spack.repo.use_repositories(str(repo_dir)):
        yield mock_repo_packages


@pytest.fixture(scope="module")
def mock_pkg_names():
    repo = spack.repo.PATH.get_repo("builtin.mock")

    # Be sure to include virtual packages since packages with stand-alone
    # tests may inherit additional tests from the virtuals they provide,
    # such as packages that implement `mpi`.
    return {
        name
        for name in repo.all_package_names(include_virtuals=True)
        if not name.startswith("mockpkg-")
    }


def split(output):
    """Split command line output into an array."""
    output = output.strip()
    return re.split(r"\s+", output) if output else []


pkg = spack.main.SpackCommand("pkg")


def test_packages_path():
    assert spack.repo.packages_path() == spack.repo.PATH.get_repo("builtin").packages_path


def test_mock_packages_path(mock_packages):
    assert spack.repo.packages_path() == spack.repo.PATH.get_repo("builtin.mock").packages_path


def test_pkg_add(git, mock_pkg_git_repo):
    with working_dir(mock_pkg_git_repo):
        mkdirp("mockpkg-e")
        with open("mockpkg-e/package.py", "w") as f:
            f.write(pkg_template.format(name="PkgE"))

    pkg("add", "mockpkg-e")

    with working_dir(mock_pkg_git_repo):
        try:
            assert "A  mockpkg-e/package.py" in git("status", "--short", output=str)
        finally:
            shutil.rmtree("mockpkg-e")
            # Removing a package mid-run disrupts Spack's caching
            if spack.repo.PATH.repos[0]._fast_package_checker:
                spack.repo.PATH.repos[0]._fast_package_checker.invalidate()

    with pytest.raises(spack.main.SpackCommandError):
        pkg("add", "does-not-exist")


@pytest.mark.not_on_windows("stdout format conflict")
def test_pkg_list(mock_pkg_git_repo, mock_pkg_names):
    out = split(pkg("list", "HEAD^^"))
    assert sorted(mock_pkg_names) == sorted(out)

    out = split(pkg("list", "HEAD^"))
    assert sorted(mock_pkg_names.union(["mockpkg-a", "mockpkg-b", "mockpkg-c"])) == sorted(out)

    out = split(pkg("list", "HEAD"))
    assert sorted(mock_pkg_names.union(["mockpkg-a", "mockpkg-b", "mockpkg-d"])) == sorted(out)

    # test with three dots to make sure pkg calls `git merge-base`
    out = split(pkg("list", "HEAD^^..."))
    assert sorted(mock_pkg_names) == sorted(out)


@pytest.mark.not_on_windows("stdout format conflict")
def test_pkg_diff(mock_pkg_git_repo, mock_pkg_names):
    out = split(pkg("diff", "HEAD^^", "HEAD^"))
    assert out == ["HEAD^:", "mockpkg-a", "mockpkg-b", "mockpkg-c"]

    out = split(pkg("diff", "HEAD^^", "HEAD"))
    assert out == ["HEAD:", "mockpkg-a", "mockpkg-b", "mockpkg-d"]

    out = split(pkg("diff", "HEAD^", "HEAD"))
    assert out == ["HEAD^:", "mockpkg-c", "HEAD:", "mockpkg-d"]


@pytest.mark.not_on_windows("stdout format conflict")
def test_pkg_added(mock_pkg_git_repo):
    out = split(pkg("added", "HEAD^^", "HEAD^"))
    assert ["mockpkg-a", "mockpkg-b", "mockpkg-c"] == out

    out = split(pkg("added", "HEAD^^", "HEAD"))
    assert ["mockpkg-a", "mockpkg-b", "mockpkg-d"] == out

    out = split(pkg("added", "HEAD^", "HEAD"))
    assert ["mockpkg-d"] == out

    out = split(pkg("added", "HEAD", "HEAD"))
    assert out == []


@pytest.mark.not_on_windows("stdout format conflict")
def test_pkg_removed(mock_pkg_git_repo):
    out = split(pkg("removed", "HEAD^^", "HEAD^"))
    assert out == []

    out = split(pkg("removed", "HEAD^^", "HEAD"))
    assert out == []

    out = split(pkg("removed", "HEAD^", "HEAD"))
    assert out == ["mockpkg-c"]


@pytest.mark.not_on_windows("stdout format conflict")
def test_pkg_changed(mock_pkg_git_repo):
    out = split(pkg("changed", "HEAD^^", "HEAD^"))
    assert out == []

    out = split(pkg("changed", "--type", "c", "HEAD^^", "HEAD^"))
    assert out == []

    out = split(pkg("changed", "--type", "a", "HEAD^^", "HEAD^"))
    assert out == ["mockpkg-a", "mockpkg-b", "mockpkg-c"]

    out = split(pkg("changed", "--type", "r", "HEAD^^", "HEAD^"))
    assert out == []

    out = split(pkg("changed", "--type", "ar", "HEAD^^", "HEAD^"))
    assert out == ["mockpkg-a", "mockpkg-b", "mockpkg-c"]

    out = split(pkg("changed", "--type", "arc", "HEAD^^", "HEAD^"))
    assert out == ["mockpkg-a", "mockpkg-b", "mockpkg-c"]

    out = split(pkg("changed", "HEAD^", "HEAD"))
    assert out == ["mockpkg-b"]

    out = split(pkg("changed", "--type", "c", "HEAD^", "HEAD"))
    assert out == ["mockpkg-b"]

    out = split(pkg("changed", "--type", "a", "HEAD^", "HEAD"))
    assert out == ["mockpkg-d"]

    out = split(pkg("changed", "--type", "r", "HEAD^", "HEAD"))
    assert out == ["mockpkg-c"]

    out = split(pkg("changed", "--type", "ar", "HEAD^", "HEAD"))
    assert out == ["mockpkg-c", "mockpkg-d"]

    out = split(pkg("changed", "--type", "arc", "HEAD^", "HEAD"))
    assert out == ["mockpkg-b", "mockpkg-c", "mockpkg-d"]

    # invalid type argument
    with pytest.raises(spack.main.SpackCommandError):
        pkg("changed", "--type", "foo")


def test_pkg_fails_when_not_git_repo(monkeypatch):
    monkeypatch.setattr(spack.cmd, "spack_is_git_repo", lambda: False)
    with pytest.raises(spack.main.SpackCommandError):
        pkg("added")


def test_pkg_source_requires_one_arg(mock_packages):
    with pytest.raises(spack.main.SpackCommandError):
        pkg("source", "a", "b")

    with pytest.raises(spack.main.SpackCommandError):
        pkg("source", "--canonical", "a", "b")


def test_pkg_source(mock_packages):
    fake_source = pkg("source", "fake")

    fake_file = spack.repo.PATH.filename_for_package_name("fake")
    with open(fake_file) as f:
        contents = f.read()
        assert fake_source == contents


def test_pkg_canonical_source(mock_packages):
    source = pkg("source", "multimethod")
    assert '@when("@2.0")' in source
    assert "Check that multimethods work with boolean values" in source

    canonical_1 = pkg("source", "--canonical", "multimethod@1.0")
    assert "@when" not in canonical_1
    assert "should_not_be_reached by diamond inheritance test" not in canonical_1
    assert "return 'base@1.0'" in canonical_1
    assert "return 'base@2.0'" not in canonical_1
    assert "return 'first_parent'" not in canonical_1
    assert "'should_not_be_reached by diamond inheritance test'" not in canonical_1

    canonical_2 = pkg("source", "--canonical", "multimethod@2.0")
    assert "@when" not in canonical_2
    assert "return 'base@1.0'" not in canonical_2
    assert "return 'base@2.0'" in canonical_2
    assert "return 'first_parent'" in canonical_2
    assert "'should_not_be_reached by diamond inheritance test'" not in canonical_2

    canonical_3 = pkg("source", "--canonical", "multimethod@3.0")
    assert "@when" not in canonical_3
    assert "return 'base@1.0'" not in canonical_3
    assert "return 'base@2.0'" not in canonical_3
    assert "return 'first_parent'" not in canonical_3
    assert "'should_not_be_reached by diamond inheritance test'" not in canonical_3

    canonical_4 = pkg("source", "--canonical", "multimethod@4.0")
    assert "@when" not in canonical_4
    assert "return 'base@1.0'" not in canonical_4
    assert "return 'base@2.0'" not in canonical_4
    assert "return 'first_parent'" not in canonical_4
    assert "'should_not_be_reached by diamond inheritance test'" in canonical_4


def test_pkg_hash(mock_packages):
    output = pkg("hash", "pkg-a", "pkg-b").strip().split()
    assert len(output) == 2 and all(len(elt) == 32 for elt in output)

    output = pkg("hash", "multimethod").strip().split()
    assert len(output) == 1 and all(len(elt) == 32 for elt in output)


@pytest.mark.skipif(not spack.cmd.pkg.get_grep(), reason="grep is not installed")
def test_pkg_grep(mock_packages, capfd):
    # only splice-* mock packages have the string "splice" in them
    pkg("grep", "-l", "splice", output=str)
    output, _ = capfd.readouterr()
    assert output.strip() == "\n".join(
        spack.repo.PATH.get_pkg_class(name).module.__file__
        for name in ["splice-a", "splice-h", "splice-t", "splice-vh", "splice-vt", "splice-z"]
    )

    # ensure that this string isn't fouhnd
    pkg("grep", "abcdefghijklmnopqrstuvwxyz", output=str, fail_on_error=False)
    assert pkg.returncode == 1
    output, _ = capfd.readouterr()
    assert output.strip() == ""

    # ensure that we return > 1 for an error
    pkg("grep", "--foobarbaz-not-an-option", output=str, fail_on_error=False)
    assert pkg.returncode == 2
