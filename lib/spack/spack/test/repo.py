# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib

import pytest

import spack.package_base
import spack.paths
import spack.repo
import spack.spec
import spack.util.file_cache


@pytest.fixture(params=["packages", "", "foo"])
def extra_repo(tmp_path_factory, request):
    repo_namespace = "extra_test_repo"
    repo_dir = tmp_path_factory.mktemp(repo_namespace)
    cache_dir = tmp_path_factory.mktemp("cache")
    (repo_dir / request.param).mkdir(parents=True, exist_ok=True)
    if request.param == "packages":
        (repo_dir / "repo.yaml").write_text(
            """
repo:
  namespace: extra_test_repo
"""
        )
    else:
        (repo_dir / "repo.yaml").write_text(
            f"""
repo:
  namespace: extra_test_repo
  subdirectory: '{request.param}'
"""
        )
    repo_cache = spack.util.file_cache.FileCache(str(cache_dir))
    return spack.repo.Repo(str(repo_dir), cache=repo_cache), request.param


def test_repo_getpkg(mutable_mock_repo):
    mutable_mock_repo.get_pkg_class("pkg-a")
    mutable_mock_repo.get_pkg_class("builtin.mock.pkg-a")


def test_repo_multi_getpkg(mutable_mock_repo, extra_repo):
    mutable_mock_repo.put_first(extra_repo[0])
    mutable_mock_repo.get_pkg_class("pkg-a")
    mutable_mock_repo.get_pkg_class("builtin.mock.pkg-a")


def test_repo_multi_getpkgclass(mutable_mock_repo, extra_repo):
    mutable_mock_repo.put_first(extra_repo[0])
    mutable_mock_repo.get_pkg_class("pkg-a")
    mutable_mock_repo.get_pkg_class("builtin.mock.pkg-a")


def test_repo_pkg_with_unknown_namespace(mutable_mock_repo):
    with pytest.raises(spack.repo.UnknownNamespaceError):
        mutable_mock_repo.get_pkg_class("unknown.pkg-a")


def test_repo_unknown_pkg(mutable_mock_repo):
    with pytest.raises(spack.repo.UnknownPackageError):
        mutable_mock_repo.get_pkg_class("builtin.mock.nonexistentpackage")


@pytest.mark.maybeslow
def test_repo_last_mtime():
    latest_mtime = max(
        os.path.getmtime(p.module.__file__) for p in spack.repo.PATH.all_package_classes()
    )
    assert spack.repo.PATH.last_mtime() == latest_mtime


def test_repo_invisibles(mutable_mock_repo, extra_repo):
    with open(os.path.join(extra_repo[0].root, extra_repo[1], ".invisible"), "w"):
        pass
    extra_repo[0].all_package_names()


@pytest.mark.parametrize("attr_name,exists", [("cmake", True), ("__sphinx_mock__", False)])
@pytest.mark.regression("20661")
def test_namespace_hasattr(attr_name, exists, mutable_mock_repo):
    # Check that we don't fail on 'hasattr' checks because
    # of a custom __getattr__ implementation
    nms = spack.repo.SpackNamespace("spack.pkg.builtin.mock")
    assert hasattr(nms, attr_name) == exists


@pytest.mark.regression("24552")
def test_all_package_names_is_cached_correctly():
    assert "mpi" in spack.repo.all_package_names(include_virtuals=True)
    assert "mpi" not in spack.repo.all_package_names(include_virtuals=False)


@pytest.mark.regression("29203")
def test_use_repositories_doesnt_change_class():
    """Test that we don't create the same package module and class multiple times
    when swapping repositories.
    """
    zlib_cls_outer = spack.repo.PATH.get_pkg_class("zlib")
    current_paths = [r.root for r in spack.repo.PATH.repos]
    with spack.repo.use_repositories(*current_paths):
        zlib_cls_inner = spack.repo.PATH.get_pkg_class("zlib")
    assert id(zlib_cls_inner) == id(zlib_cls_outer)


def test_import_repo_prefixes_as_python_modules(mock_packages):
    import spack.pkg.builtin.mock

    assert isinstance(spack.pkg, spack.repo.SpackNamespace)
    assert isinstance(spack.pkg.builtin, spack.repo.SpackNamespace)
    assert isinstance(spack.pkg.builtin.mock, spack.repo.SpackNamespace)


def test_absolute_import_spack_packages_as_python_modules(mock_packages):
    import spack.pkg.builtin.mock.mpileaks

    assert hasattr(spack.pkg.builtin.mock, "mpileaks")
    assert hasattr(spack.pkg.builtin.mock.mpileaks, "Mpileaks")
    assert isinstance(spack.pkg.builtin.mock.mpileaks.Mpileaks, spack.package_base.PackageMeta)
    assert issubclass(spack.pkg.builtin.mock.mpileaks.Mpileaks, spack.package_base.PackageBase)


def test_relative_import_spack_packages_as_python_modules(mock_packages):
    from spack.pkg.builtin.mock.mpileaks import Mpileaks

    assert isinstance(Mpileaks, spack.package_base.PackageMeta)
    assert issubclass(Mpileaks, spack.package_base.PackageBase)


def test_get_all_mock_packages(mock_packages):
    """Get the mock packages once each too."""
    for name in mock_packages.all_package_names():
        mock_packages.get_pkg_class(name)


def test_repo_path_handles_package_removal(tmpdir, mock_packages):
    builder = spack.repo.MockRepositoryBuilder(tmpdir, namespace="removal")
    builder.add_package("pkg-c")
    with spack.repo.use_repositories(builder.root, override=False) as repos:
        r = repos.repo_for_pkg("pkg-c")
        assert r.namespace == "removal"

    builder.remove("pkg-c")
    with spack.repo.use_repositories(builder.root, override=False) as repos:
        r = repos.repo_for_pkg("pkg-c")
        assert r.namespace == "builtin.mock"


def test_repo_dump_virtuals(tmpdir, mutable_mock_repo, mock_packages, ensure_debug, capsys):
    # Start with a package-less virtual
    vspec = spack.spec.Spec("something")
    mutable_mock_repo.dump_provenance(vspec, tmpdir)
    captured = capsys.readouterr()[1]
    assert "does not have a package" in captured

    # Now with a virtual with a package
    vspec = spack.spec.Spec("externalvirtual")
    mutable_mock_repo.dump_provenance(vspec, tmpdir)
    captured = capsys.readouterr()[1]
    assert "Installing" in captured
    assert "package.py" in os.listdir(tmpdir), "Expected the virtual's package to be copied"


@pytest.mark.parametrize(
    "repo_paths,namespaces",
    [
        ([spack.paths.packages_path], ["builtin"]),
        ([spack.paths.mock_packages_path], ["builtin.mock"]),
        ([spack.paths.packages_path, spack.paths.mock_packages_path], ["builtin", "builtin.mock"]),
        ([spack.paths.mock_packages_path, spack.paths.packages_path], ["builtin.mock", "builtin"]),
    ],
)
def test_repository_construction_doesnt_use_globals(
    nullify_globals, tmp_path, repo_paths, namespaces
):
    repo_cache = spack.util.file_cache.FileCache(str(tmp_path / "cache"))
    repo_path = spack.repo.RepoPath(*repo_paths, cache=repo_cache)
    assert len(repo_path.repos) == len(namespaces)
    assert [x.namespace for x in repo_path.repos] == namespaces


@pytest.mark.parametrize("method_name", ["dirname_for_package_name", "filename_for_package_name"])
def test_path_computation_with_names(method_name, mock_repo_path):
    """Tests that repositories can compute the correct paths when using both fully qualified
    names and unqualified names.
    """
    repo_path = spack.repo.RepoPath(mock_repo_path, cache=None)
    method = getattr(repo_path, method_name)
    unqualified = method("mpileaks")
    qualified = method("builtin.mock.mpileaks")
    assert qualified == unqualified


def test_use_repositories_and_import():
    """Tests that use_repositories changes the import search too"""
    import spack.paths

    repo_dir = pathlib.Path(spack.paths.repos_path)
    with spack.repo.use_repositories(str(repo_dir / "compiler_runtime.test")):
        import spack.pkg.compiler_runtime.test.gcc_runtime

    with spack.repo.use_repositories(str(repo_dir / "builtin.mock")):
        import spack.pkg.builtin.mock.cmake


@pytest.mark.usefixtures("nullify_globals")
class TestRepo:
    """Test that the Repo class work correctly, and does not depend on globals,
    except the REPOS_FINDER.
    """

    def test_creation(self, mock_test_cache):
        repo = spack.repo.Repo(spack.paths.mock_packages_path, cache=mock_test_cache)
        assert repo.config_file.endswith("repo.yaml")
        assert repo.namespace == "builtin.mock"

    @pytest.mark.parametrize(
        "name,expected", [("mpi", True), ("mpich", False), ("mpileaks", False)]
    )
    @pytest.mark.parametrize("repo_cls", [spack.repo.Repo, spack.repo.RepoPath])
    def test_is_virtual(self, repo_cls, name, expected, mock_test_cache):
        repo = repo_cls(spack.paths.mock_packages_path, cache=mock_test_cache)
        assert repo.is_virtual(name) is expected
        assert repo.is_virtual_safe(name) is expected

    @pytest.mark.parametrize(
        "module_name,expected",
        [
            ("dla_future", "dla-future"),
            ("num7zip", "7zip"),
            # If no package is there, None is returned
            ("unknown", None),
        ],
    )
    def test_real_name(self, module_name, expected, mock_test_cache):
        """Test that we can correctly compute the 'real' name of a package, from the one
        used to import the Python module.
        """
        repo = spack.repo.Repo(spack.paths.mock_packages_path, cache=mock_test_cache)
        assert repo.real_name(module_name) == expected

    @pytest.mark.parametrize("name", ["mpileaks", "7zip", "dla-future"])
    def test_get(self, name, mock_test_cache):
        repo = spack.repo.Repo(spack.paths.mock_packages_path, cache=mock_test_cache)
        mock_spec = spack.spec.Spec(name)
        mock_spec._mark_concrete()
        pkg = repo.get(mock_spec)
        assert pkg.__class__ == repo.get_pkg_class(name)

    @pytest.mark.parametrize("virtual_name,expected", [("mpi", ["mpich", "zmpi"])])
    def test_providers(self, virtual_name, expected, mock_test_cache):
        repo = spack.repo.Repo(spack.paths.mock_packages_path, cache=mock_test_cache)
        provider_names = {x.name for x in repo.providers_for(virtual_name)}
        assert provider_names.issuperset(expected)

    @pytest.mark.parametrize(
        "extended,expected",
        [("python", ["py-extension1", "python-venv"]), ("perl", ["perl-extension"])],
    )
    @pytest.mark.parametrize("repo_cls", [spack.repo.Repo, spack.repo.RepoPath])
    def test_extensions(self, repo_cls, extended, expected, mock_test_cache):
        repo = repo_cls(spack.paths.mock_packages_path, cache=mock_test_cache)
        provider_names = {x.name for x in repo.extensions_for(extended)}
        assert provider_names.issuperset(expected)

    @pytest.mark.parametrize("repo_cls", [spack.repo.Repo, spack.repo.RepoPath])
    def test_all_package_names(self, repo_cls, mock_test_cache):
        repo = repo_cls(spack.paths.mock_packages_path, cache=mock_test_cache)
        all_names = repo.all_package_names(include_virtuals=True)
        real_names = repo.all_package_names(include_virtuals=False)
        assert set(all_names).issuperset(real_names)
        for name in set(all_names) - set(real_names):
            assert repo.is_virtual(name)
            assert repo.is_virtual_safe(name)

    @pytest.mark.parametrize("repo_cls", [spack.repo.Repo, spack.repo.RepoPath])
    def test_packages_with_tags(self, repo_cls, mock_test_cache):
        repo = repo_cls(spack.paths.mock_packages_path, cache=mock_test_cache)
        r1 = repo.packages_with_tags("tag1")
        r2 = repo.packages_with_tags("tag1", "tag2")
        assert "mpich" in r1 and "mpich" in r2
        assert "mpich2" in r1 and "mpich2" not in r2
        assert set(r2).issubset(r1)


@pytest.mark.usefixtures("nullify_globals")
class TestRepoPath:
    def test_creation_from_string(self, mock_test_cache):
        repo = spack.repo.RepoPath(spack.paths.mock_packages_path, cache=mock_test_cache)
        assert len(repo.repos) == 1
        assert repo.repos[0]._finder is repo
        assert repo.by_namespace["spack.pkg.builtin.mock"] is repo.repos[0]

    def test_get_repo(self, mock_test_cache):
        repo = spack.repo.RepoPath(spack.paths.mock_packages_path, cache=mock_test_cache)
        # builtin.mock is there
        assert repo.get_repo("builtin.mock") is repo.repos[0]
        # foo is not there, raise
        with pytest.raises(spack.repo.UnknownNamespaceError):
            repo.get_repo("foo")
