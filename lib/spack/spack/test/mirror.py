# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os

import pytest

from llnl.util.symlink import resolve_link_target_relative_to_the_link

import spack.caches
import spack.config
import spack.fetch_strategy
import spack.mirror
import spack.patch
import spack.stage
import spack.util.executable
import spack.util.spack_json as sjson
import spack.util.url as url_util
from spack.spec import Spec
from spack.util.executable import which
from spack.util.spack_yaml import SpackYAMLError

pytestmark = [pytest.mark.usefixtures("mutable_config", "mutable_mock_repo")]

# paths in repos that shouldn't be in the mirror tarballs.
exclude = [".hg", ".git", ".svn"]


repos = {}


def set_up_package(name, repository, url_attr):
    """Set up a mock package to be mirrored.
    Each package needs us to:

    1. Set up a mock repo/archive to fetch from.
    2. Point the package's version args at that repo.
    """
    # Set up packages to point at mock repos.
    s = Spec(name).concretized()
    repos[name] = repository

    # change the fetch args of the first (only) version.
    assert len(s.package.versions) == 1

    v = next(iter(s.package.versions))
    s.package.versions[v][url_attr] = repository.url


def check_mirror():
    with spack.stage.Stage("spack-mirror-test") as stage:
        mirror_root = os.path.join(stage.path, "test-mirror")
        # register mirror with spack config
        mirrors = {"spack-mirror-test": url_util.path_to_file_url(mirror_root)}
        with spack.config.override("mirrors", mirrors):
            with spack.config.override("config:checksum", False):
                specs = [Spec(x).concretized() for x in repos]
                spack.mirror.create(mirror_root, specs)

            # Stage directory exists
            assert os.path.isdir(mirror_root)

            for spec in specs:
                fetcher = spec.package.fetcher
                per_package_ref = os.path.join(spec.name, "-".join([spec.name, str(spec.version)]))
                mirror_layout = spack.mirror.default_mirror_layout(fetcher, per_package_ref)
                expected_path = os.path.join(mirror_root, mirror_layout.path)
                assert os.path.exists(expected_path)

            # Now try to fetch each package.
            for name, mock_repo in repos.items():
                spec = Spec(name).concretized()
                pkg = spec.package

                with spack.config.override("config:checksum", False):
                    with pkg.stage:
                        pkg.do_stage(mirror_only=True)

                        # Compare the original repo with the expanded archive
                        original_path = mock_repo.path
                        if "svn" in name:
                            # have to check out the svn repo to compare.
                            original_path = os.path.join(mock_repo.path, "checked_out")

                            svn = which("svn", required=True)
                            svn("checkout", mock_repo.url, original_path)

                        dcmp = filecmp.dircmp(original_path, pkg.stage.source_path)

                        # make sure there are no new files in the expanded
                        # tarball
                        assert not dcmp.right_only
                        # and that all original files are present.
                        assert all(left in exclude for left in dcmp.left_only)


def test_url_mirror(mock_archive):
    set_up_package("trivial-install-test-package", mock_archive, "url")
    check_mirror()
    repos.clear()


def test_git_mirror(git, mock_git_repository):
    set_up_package("git-test", mock_git_repository, "git")
    check_mirror()
    repos.clear()


def test_svn_mirror(mock_svn_repository):
    set_up_package("svn-test", mock_svn_repository, "svn")
    check_mirror()
    repos.clear()


def test_hg_mirror(mock_hg_repository):
    set_up_package("hg-test", mock_hg_repository, "hg")
    check_mirror()
    repos.clear()


def test_all_mirror(mock_git_repository, mock_svn_repository, mock_hg_repository, mock_archive):
    set_up_package("git-test", mock_git_repository, "git")
    set_up_package("svn-test", mock_svn_repository, "svn")
    set_up_package("hg-test", mock_hg_repository, "hg")
    set_up_package("trivial-install-test-package", mock_archive, "url")
    check_mirror()
    repos.clear()


@pytest.mark.parametrize(
    "mirror",
    [
        spack.mirror.Mirror(
            {"fetch": "https://example.com/fetch", "push": "https://example.com/push"}
        )
    ],
)
def test_roundtrip_mirror(mirror: spack.mirror.Mirror):
    mirror_yaml = mirror.to_yaml()
    assert spack.mirror.Mirror.from_yaml(mirror_yaml) == mirror
    mirror_json = mirror.to_json()
    assert spack.mirror.Mirror.from_json(mirror_json) == mirror


@pytest.mark.parametrize(
    "invalid_yaml", ["playing_playlist: {{ action }} playlist {{ playlist_name }}"]
)
def test_invalid_yaml_mirror(invalid_yaml):
    with pytest.raises(SpackYAMLError, match="error parsing YAML") as e:
        spack.mirror.Mirror.from_yaml(invalid_yaml)
    assert invalid_yaml in str(e.value)


@pytest.mark.parametrize("invalid_json, error_message", [("{13:", "Expecting property name")])
def test_invalid_json_mirror(invalid_json, error_message):
    with pytest.raises(sjson.SpackJSONError) as e:
        spack.mirror.Mirror.from_json(invalid_json)
    exc_msg = str(e.value)
    assert exc_msg.startswith("error parsing JSON mirror:")
    assert error_message in exc_msg


@pytest.mark.parametrize(
    "mirror_collection",
    [
        spack.mirror.MirrorCollection(
            mirrors={
                "example-mirror": spack.mirror.Mirror(
                    "https://example.com/fetch", "https://example.com/push"
                ).to_dict()
            }
        )
    ],
)
def test_roundtrip_mirror_collection(mirror_collection):
    mirror_collection_yaml = mirror_collection.to_yaml()
    assert spack.mirror.MirrorCollection.from_yaml(mirror_collection_yaml) == mirror_collection
    mirror_collection_json = mirror_collection.to_json()
    assert spack.mirror.MirrorCollection.from_json(mirror_collection_json) == mirror_collection


@pytest.mark.parametrize(
    "invalid_yaml", ["playing_playlist: {{ action }} playlist {{ playlist_name }}"]
)
def test_invalid_yaml_mirror_collection(invalid_yaml):
    with pytest.raises(SpackYAMLError, match="error parsing YAML") as e:
        spack.mirror.MirrorCollection.from_yaml(invalid_yaml)
    assert invalid_yaml in str(e.value)


@pytest.mark.parametrize("invalid_json, error_message", [("{13:", "Expecting property name")])
def test_invalid_json_mirror_collection(invalid_json, error_message):
    with pytest.raises(sjson.SpackJSONError) as e:
        spack.mirror.MirrorCollection.from_json(invalid_json)
    exc_msg = str(e.value)
    assert exc_msg.startswith("error parsing JSON mirror collection:")
    assert error_message in exc_msg


def test_mirror_archive_paths_no_version(mock_packages, mock_archive):
    spec = Spec("trivial-install-test-package@=nonexistingversion").concretized()
    fetcher = spack.fetch_strategy.URLFetchStrategy(url=mock_archive.url)
    spack.mirror.default_mirror_layout(fetcher, "per-package-ref", spec)


def test_mirror_with_url_patches(mock_packages, monkeypatch):
    spec = Spec("patch-several-dependencies").concretized()
    files_cached_in_mirror = set()

    def record_store(_class, fetcher, relative_dst, cosmetic_path=None):
        files_cached_in_mirror.add(os.path.basename(relative_dst))

    def successful_fetch(_class):
        with open(_class.stage.save_filename, "w"):
            pass

    def successful_expand(_class):
        expanded_path = os.path.join(_class.stage.path, spack.stage._source_path_subdir)
        os.mkdir(expanded_path)
        with open(os.path.join(expanded_path, "test.patch"), "w"):
            pass

    def successful_apply(*args, **kwargs):
        pass

    def successful_make_alias(*args, **kwargs):
        pass

    with spack.stage.Stage("spack-mirror-test") as stage:
        mirror_root = os.path.join(stage.path, "test-mirror")

        monkeypatch.setattr(spack.fetch_strategy.URLFetchStrategy, "fetch", successful_fetch)
        monkeypatch.setattr(spack.fetch_strategy.URLFetchStrategy, "expand", successful_expand)
        monkeypatch.setattr(spack.patch, "apply_patch", successful_apply)
        monkeypatch.setattr(spack.caches.MirrorCache, "store", record_store)
        monkeypatch.setattr(spack.mirror.DefaultLayout, "make_alias", successful_make_alias)

        with spack.config.override("config:checksum", False):
            spack.mirror.create(mirror_root, list(spec.traverse()))

        assert {
            "abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234",
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd.gz",
        }.issubset(files_cached_in_mirror)


class MockFetcher:
    """Mock fetcher object which implements the necessary functionality for
    testing MirrorCache
    """

    @staticmethod
    def archive(dst):
        with open(dst, "w"):
            pass


@pytest.mark.regression("14067")
def test_mirror_layout_make_alias(tmpdir):
    """Confirm that the cosmetic symlink created in the mirror cache (which may
    be relative) targets the storage path correctly.
    """
    alias = os.path.join("zlib", "zlib-1.2.11.tar.gz")
    path = os.path.join("_source-cache", "archive", "c3", "c3e5.tar.gz")
    cache = spack.caches.MirrorCache(root=str(tmpdir), skip_unstable_versions=False)
    layout = spack.mirror.DefaultLayout(alias, path)

    cache.store(MockFetcher(), layout.path)
    layout.make_alias(cache.root)

    link_target = resolve_link_target_relative_to_the_link(os.path.join(cache.root, layout.alias))
    assert os.path.exists(link_target)
    assert os.path.normpath(link_target) == os.path.join(cache.root, layout.path)


@pytest.mark.regression("31627")
@pytest.mark.parametrize(
    "specs,expected_specs",
    [
        (["pkg-a"], ["pkg-a@=1.0", "pkg-a@=2.0"]),
        (["pkg-a", "brillig"], ["pkg-a@=1.0", "pkg-a@=2.0", "brillig@=1.0.0", "brillig@=2.0.0"]),
    ],
)
def test_get_all_versions(specs, expected_specs):
    specs = [Spec(s) for s in specs]
    output_list = spack.mirror.get_all_versions(specs)
    output_list = [str(x) for x in output_list]
    # Compare sets since order is not important
    assert set(output_list) == set(expected_specs)


def test_update_1():
    # No change
    m = spack.mirror.Mirror("https://example.com")
    assert not m.update({"url": "https://example.com"})
    assert m.to_dict() == "https://example.com"


def test_update_2():
    # Change URL, shouldn't expand to {"url": ...} dict.
    m = spack.mirror.Mirror("https://example.com")
    assert m.update({"url": "https://example.org"})
    assert m.to_dict() == "https://example.org"
    assert m.fetch_url == "https://example.org"
    assert m.push_url == "https://example.org"


def test_update_3():
    # Change fetch url, ensure minimal config
    m = spack.mirror.Mirror("https://example.com")
    assert m.update({"url": "https://example.org"}, "fetch")
    assert m.to_dict() == {"url": "https://example.com", "fetch": "https://example.org"}
    assert m.fetch_url == "https://example.org"
    assert m.push_url == "https://example.com"


def test_update_4():
    # Change push url, ensure minimal config
    m = spack.mirror.Mirror("https://example.com")
    assert m.update({"url": "https://example.org"}, "push")
    assert m.to_dict() == {"url": "https://example.com", "push": "https://example.org"}
    assert m.push_url == "https://example.org"
    assert m.fetch_url == "https://example.com"


@pytest.mark.parametrize("direction", ["fetch", "push"])
def test_update_connection_params(direction):
    """Test whether new connection params expand the mirror config to a dict."""
    m = spack.mirror.Mirror("https://example.com")

    assert m.update(
        {
            "url": "http://example.org",
            "access_pair": ["username", "password"],
            "access_token": "token",
            "profile": "profile",
            "endpoint_url": "https://example.com",
        },
        direction,
    )

    assert m.to_dict() == {
        "url": "https://example.com",
        direction: {
            "url": "http://example.org",
            "access_pair": ["username", "password"],
            "access_token": "token",
            "profile": "profile",
            "endpoint_url": "https://example.com",
        },
    }

    assert m.get_access_pair(direction) == ["username", "password"]
    assert m.get_access_token(direction) == "token"
    assert m.get_profile(direction) == "profile"
    assert m.get_endpoint_url(direction) == "https://example.com"
