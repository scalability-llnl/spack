# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This test checks the binary packaging infrastructure
"""
import argparse
import os
import pathlib
import platform
import shutil
import urllib.error
from collections import OrderedDict

import pytest

from llnl.util import filesystem as fs
from llnl.util.symlink import readlink, symlink

import spack.binary_distribution as bindist
import spack.cmd.buildcache as buildcache
import spack.config
import spack.error
import spack.fetch_strategy
import spack.mirror
import spack.package_base
import spack.stage
import spack.util.gpg
import spack.util.url as url_util
from spack.fetch_strategy import URLFetchStrategy
from spack.installer import PackageInstaller
from spack.paths import mock_gpg_keys_path
from spack.relocate import (
    macho_find_paths,
    macho_make_paths_normal,
    macho_make_paths_relative,
    needs_binary_relocation,
    needs_text_relocation,
    relocate_links,
    relocate_text,
)
from spack.spec import Spec

pytestmark = pytest.mark.not_on_windows("does not run on windows")


@pytest.mark.usefixtures("install_mockery", "mock_gnupghome")
def test_buildcache(mock_archive, tmp_path, monkeypatch, mutable_config):
    # Install a test package
    spec = Spec("trivial-install-test-package").concretized()
    monkeypatch.setattr(spec.package, "fetcher", URLFetchStrategy(url=mock_archive.url))
    PackageInstaller([spec.package], explicit=True).install()
    pkghash = "/" + str(spec.dag_hash(7))

    # Put some non-relocatable file in there
    dummy_txt = pathlib.Path(spec.prefix) / "dummy.txt"
    dummy_txt.write_text(spec.prefix)

    # Create an absolute symlink
    linkname = os.path.join(spec.prefix, "link_to_dummy.txt")
    symlink(dummy_txt, linkname)

    # Create the build cache and put it directly into the mirror
    mirror_path = str(tmp_path / "test-mirror")
    spack.mirror.create(mirror_path, specs=[])

    # register mirror with spack config
    mirrors = {"spack-mirror-test": url_util.path_to_file_url(mirror_path)}
    spack.config.set("mirrors", mirrors)

    with spack.stage.Stage(mirrors["spack-mirror-test"], name="build_cache", keep=True):
        parser = argparse.ArgumentParser()
        buildcache.setup_parser(parser)

        create_args = ["create", "-f", "--rebuild-index", mirror_path, pkghash]
        # Create a private key to sign package with if gpg2 available
        spack.util.gpg.create(
            name="test key 1",
            expires="0",
            email="spack@googlegroups.com",
            comment="Spack test key",
        )

        args = parser.parse_args(create_args)
        buildcache.buildcache(parser, args)
        # trigger overwrite warning
        buildcache.buildcache(parser, args)

        # Uninstall the package
        spec.package.do_uninstall(force=True)

        install_args = ["install", "-f", pkghash]
        args = parser.parse_args(install_args)
        # Test install
        buildcache.buildcache(parser, args)

        files = os.listdir(spec.prefix)

        assert "link_to_dummy.txt" in files
        assert "dummy.txt" in files

        # Validate the relocation information
        buildinfo = bindist.read_buildinfo_file(spec.prefix)
        assert buildinfo["relocate_textfiles"] == ["dummy.txt"]
        assert buildinfo["relocate_links"] == ["link_to_dummy.txt"]

        args = parser.parse_args(["keys"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["list"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["list"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["list", "trivial"])
        buildcache.buildcache(parser, args)

        # Copy a key to the mirror to have something to download
        shutil.copyfile(mock_gpg_keys_path + "/external.key", mirror_path + "/external.key")

        args = parser.parse_args(["keys"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["keys", "-f"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["keys", "-i", "-t"])
        buildcache.buildcache(parser, args)


def test_relocate_text(tmp_path):
    """Tests that a text file containing the original directory of an installation, can be
    relocated to a target directory.
    """
    original_dir = "/home/spack/opt/spack"
    relocation_dir = "/opt/rh/devtoolset/"
    dummy_txt = tmp_path / "dummy.txt"
    dummy_txt.write_text(original_dir)

    relocate_text([str(dummy_txt)], {original_dir: relocation_dir})
    text = dummy_txt.read_text()

    assert relocation_dir in text
    assert original_dir not in text


def test_relocate_links(tmpdir):
    tmpdir.ensure("new_prefix_a", dir=True)

    own_prefix_path = str(tmpdir.join("prefix_a", "file"))
    dep_prefix_path = str(tmpdir.join("prefix_b", "file"))
    new_own_prefix_path = str(tmpdir.join("new_prefix_a", "file"))
    new_dep_prefix_path = str(tmpdir.join("new_prefix_b", "file"))
    system_path = os.path.join(os.path.sep, "system", "path")

    fs.touchp(own_prefix_path)
    fs.touchp(new_own_prefix_path)
    fs.touchp(dep_prefix_path)
    fs.touchp(new_dep_prefix_path)

    # Old prefixes to new prefixes
    prefix_to_prefix = OrderedDict(
        [
            # map <tmpdir>/prefix_a -> <tmpdir>/new_prefix_a
            (str(tmpdir.join("prefix_a")), str(tmpdir.join("new_prefix_a"))),
            # map <tmpdir>/prefix_b -> <tmpdir>/new_prefix_b
            (str(tmpdir.join("prefix_b")), str(tmpdir.join("new_prefix_b"))),
            # map <tmpdir> -> /fallback/path -- this is just to see we respect order.
            (str(tmpdir), os.path.join(os.path.sep, "fallback", "path")),
        ]
    )

    with tmpdir.join("new_prefix_a").as_cwd():
        # To be relocated
        os.symlink(own_prefix_path, "to_self")
        os.symlink(dep_prefix_path, "to_dependency")

        # To be ignored
        os.symlink(system_path, "to_system")
        os.symlink("relative", "to_self_but_relative")

        relocate_links(["to_self", "to_dependency", "to_system"], prefix_to_prefix)

        # These two are relocated
        assert readlink("to_self") == str(tmpdir.join("new_prefix_a", "file"))
        assert readlink("to_dependency") == str(tmpdir.join("new_prefix_b", "file"))

        # These two are not.
        assert readlink("to_system") == system_path
        assert readlink("to_self_but_relative") == "relative"


def test_needs_relocation():
    assert needs_binary_relocation("application", "x-sharedlib")
    assert needs_binary_relocation("application", "x-executable")
    assert not needs_binary_relocation("application", "x-octet-stream")
    assert not needs_binary_relocation("text", "x-")
    assert needs_text_relocation("text", "x-")
    assert not needs_text_relocation("symbolic link to", "x-")
    assert needs_binary_relocation("application", "x-mach-binary")


def test_replace_paths(tmpdir):
    with tmpdir.as_cwd():
        suffix = "dylib" if platform.system().lower() == "darwin" else "so"
        hash_a = "53moz6jwnw3xpiztxwhc4us26klribws"
        hash_b = "tk62dzu62kd4oh3h3heelyw23hw2sfee"
        hash_c = "hdkhduizmaddpog6ewdradpobnbjwsjl"
        hash_d = "hukkosc7ahff7o65h6cdhvcoxm57d4bw"
        hash_loco = "zy4oigsc4eovn5yhr2lk4aukwzoespob"

        prefix2hash = {}

        old_spack_dir = os.path.join(f"{tmpdir}", "Users", "developer", "spack")
        fs.mkdirp(old_spack_dir)

        oldprefix_a = os.path.join(f"{old_spack_dir}", f"pkgA-{hash_a}")
        oldlibdir_a = os.path.join(f"{oldprefix_a}", "lib")
        fs.mkdirp(oldlibdir_a)
        prefix2hash[str(oldprefix_a)] = hash_a

        oldprefix_b = os.path.join(f"{old_spack_dir}", f"pkgB-{hash_b}")
        oldlibdir_b = os.path.join(f"{oldprefix_b}", "lib")
        fs.mkdirp(oldlibdir_b)
        prefix2hash[str(oldprefix_b)] = hash_b

        oldprefix_c = os.path.join(f"{old_spack_dir}", f"pkgC-{hash_c}")
        oldlibdir_c = os.path.join(f"{oldprefix_c}", "lib")
        oldlibdir_cc = os.path.join(f"{oldlibdir_c}", "C")
        fs.mkdirp(oldlibdir_c)
        prefix2hash[str(oldprefix_c)] = hash_c

        oldprefix_d = os.path.join(f"{old_spack_dir}", f"pkgD-{hash_d}")
        oldlibdir_d = os.path.join(f"{oldprefix_d}", "lib")
        fs.mkdirp(oldlibdir_d)
        prefix2hash[str(oldprefix_d)] = hash_d

        oldprefix_local = os.path.join(f"{tmpdir}", "usr", "local")
        oldlibdir_local = os.path.join(f"{oldprefix_local}", "lib")
        fs.mkdirp(oldlibdir_local)
        prefix2hash[str(oldprefix_local)] = hash_loco
        libfile_a = f"libA.{suffix}"
        libfile_b = f"libB.{suffix}"
        libfile_c = f"libC.{suffix}"
        libfile_d = f"libD.{suffix}"
        libfile_loco = f"libloco.{suffix}"
        old_libnames = [
            os.path.join(oldlibdir_a, libfile_a),
            os.path.join(oldlibdir_b, libfile_b),
            os.path.join(oldlibdir_c, libfile_c),
            os.path.join(oldlibdir_d, libfile_d),
            os.path.join(oldlibdir_local, libfile_loco),
        ]

        for old_libname in old_libnames:
            with open(old_libname, "a"):
                os.utime(old_libname, None)

        hash2prefix = dict()

        new_spack_dir = os.path.join(f"{tmpdir}", "Users", "Shared", "spack")
        fs.mkdirp(new_spack_dir)

        prefix_a = os.path.join(new_spack_dir, f"pkgA-{hash_a}")
        libdir_a = os.path.join(prefix_a, "lib")
        fs.mkdirp(libdir_a)
        hash2prefix[hash_a] = str(prefix_a)

        prefix_b = os.path.join(new_spack_dir, f"pkgB-{hash_b}")
        libdir_b = os.path.join(prefix_b, "lib")
        fs.mkdirp(libdir_b)
        hash2prefix[hash_b] = str(prefix_b)

        prefix_c = os.path.join(new_spack_dir, f"pkgC-{hash_c}")
        libdir_c = os.path.join(prefix_c, "lib")
        libdir_cc = os.path.join(libdir_c, "C")
        fs.mkdirp(libdir_cc)
        hash2prefix[hash_c] = str(prefix_c)

        prefix_d = os.path.join(new_spack_dir, f"pkgD-{hash_d}")
        libdir_d = os.path.join(prefix_d, "lib")
        fs.mkdirp(libdir_d)
        hash2prefix[hash_d] = str(prefix_d)

        prefix_local = os.path.join(f"{tmpdir}", "usr", "local")
        libdir_local = os.path.join(prefix_local, "lib")
        fs.mkdirp(libdir_local)
        hash2prefix[hash_loco] = str(prefix_local)

        new_libnames = [
            os.path.join(libdir_a, libfile_a),
            os.path.join(libdir_b, libfile_b),
            os.path.join(libdir_cc, libfile_c),
            os.path.join(libdir_d, libfile_d),
            os.path.join(libdir_local, libfile_loco),
        ]

        for new_libname in new_libnames:
            with open(new_libname, "a"):
                os.utime(new_libname, None)

        prefix2prefix = dict()
        for prefix, hash in prefix2hash.items():
            prefix2prefix[prefix] = hash2prefix[hash]

        out_dict = macho_find_paths(
            [oldlibdir_a, oldlibdir_b, oldlibdir_c, oldlibdir_cc, oldlibdir_local],
            [
                os.path.join(oldlibdir_a, libfile_a),
                os.path.join(oldlibdir_b, libfile_b),
                os.path.join(oldlibdir_local, libfile_loco),
            ],
            os.path.join(oldlibdir_cc, libfile_c),
            old_spack_dir,
            prefix2prefix,
        )
        assert out_dict == {
            oldlibdir_a: libdir_a,
            oldlibdir_b: libdir_b,
            oldlibdir_c: libdir_c,
            oldlibdir_cc: libdir_cc,
            libdir_local: libdir_local,
            os.path.join(oldlibdir_a, libfile_a): os.path.join(libdir_a, libfile_a),
            os.path.join(oldlibdir_b, libfile_b): os.path.join(libdir_b, libfile_b),
            os.path.join(oldlibdir_local, libfile_loco): os.path.join(libdir_local, libfile_loco),
            os.path.join(oldlibdir_cc, libfile_c): os.path.join(libdir_cc, libfile_c),
        }

        out_dict = macho_find_paths(
            [oldlibdir_a, oldlibdir_b, oldlibdir_c, oldlibdir_cc, oldlibdir_local],
            [
                os.path.join(oldlibdir_a, libfile_a),
                os.path.join(oldlibdir_b, libfile_b),
                os.path.join(oldlibdir_cc, libfile_c),
                os.path.join(oldlibdir_local, libfile_loco),
            ],
            None,
            old_spack_dir,
            prefix2prefix,
        )
        assert out_dict == {
            oldlibdir_a: libdir_a,
            oldlibdir_b: libdir_b,
            oldlibdir_c: libdir_c,
            oldlibdir_cc: libdir_cc,
            libdir_local: libdir_local,
            os.path.join(oldlibdir_a, libfile_a): os.path.join(libdir_a, libfile_a),
            os.path.join(oldlibdir_b, libfile_b): os.path.join(libdir_b, libfile_b),
            os.path.join(oldlibdir_local, libfile_loco): os.path.join(libdir_local, libfile_loco),
            os.path.join(oldlibdir_cc, libfile_c): os.path.join(libdir_cc, libfile_c),
        }

        out_dict = macho_find_paths(
            [oldlibdir_a, oldlibdir_b, oldlibdir_c, oldlibdir_cc, oldlibdir_local],
            [
                f"@rpath/{libfile_a}",
                f"@rpath/{libfile_b}",
                f"@rpath/{libfile_c}",
                f"@rpath/{libfile_loco}",
            ],
            None,
            old_spack_dir,
            prefix2prefix,
        )

        assert out_dict == {
            f"@rpath/{libfile_a}": f"@rpath/{libfile_a}",
            f"@rpath/{libfile_b}": f"@rpath/{libfile_b}",
            f"@rpath/{libfile_c}": f"@rpath/{libfile_c}",
            f"@rpath/{libfile_loco}": f"@rpath/{libfile_loco}",
            oldlibdir_a: libdir_a,
            oldlibdir_b: libdir_b,
            oldlibdir_c: libdir_c,
            oldlibdir_cc: libdir_cc,
            libdir_local: libdir_local,
        }

        out_dict = macho_find_paths(
            [oldlibdir_a, oldlibdir_b, oldlibdir_d, oldlibdir_local],
            [f"@rpath/{libfile_a}", f"@rpath/{libfile_b}", f"@rpath/{libfile_loco}"],
            None,
            old_spack_dir,
            prefix2prefix,
        )
        assert out_dict == {
            f"@rpath/{libfile_a}": f"@rpath/{libfile_a}",
            f"@rpath/{libfile_b}": f"@rpath/{libfile_b}",
            f"@rpath/{libfile_loco}": f"@rpath/{libfile_loco}",
            oldlibdir_a: libdir_a,
            oldlibdir_b: libdir_b,
            oldlibdir_d: libdir_d,
            libdir_local: libdir_local,
        }


def test_macho_make_paths():
    out = macho_make_paths_relative(
        "/Users/Shared/spack/pkgC/lib/libC.dylib",
        "/Users/Shared/spack",
        ("/Users/Shared/spack/pkgA/lib", "/Users/Shared/spack/pkgB/lib", "/usr/local/lib"),
        (
            "/Users/Shared/spack/pkgA/libA.dylib",
            "/Users/Shared/spack/pkgB/libB.dylib",
            "/usr/local/lib/libloco.dylib",
        ),
        "/Users/Shared/spack/pkgC/lib/libC.dylib",
    )
    assert out == {
        "/Users/Shared/spack/pkgA/lib": "@loader_path/../../pkgA/lib",
        "/Users/Shared/spack/pkgB/lib": "@loader_path/../../pkgB/lib",
        "/usr/local/lib": "/usr/local/lib",
        "/Users/Shared/spack/pkgA/libA.dylib": "@loader_path/../../pkgA/libA.dylib",
        "/Users/Shared/spack/pkgB/libB.dylib": "@loader_path/../../pkgB/libB.dylib",
        "/usr/local/lib/libloco.dylib": "/usr/local/lib/libloco.dylib",
        "/Users/Shared/spack/pkgC/lib/libC.dylib": "@rpath/libC.dylib",
    }

    out = macho_make_paths_normal(
        "/Users/Shared/spack/pkgC/lib/libC.dylib",
        ("@loader_path/../../pkgA/lib", "@loader_path/../../pkgB/lib", "/usr/local/lib"),
        (
            "@loader_path/../../pkgA/libA.dylib",
            "@loader_path/../../pkgB/libB.dylib",
            "/usr/local/lib/libloco.dylib",
        ),
        "@rpath/libC.dylib",
    )

    assert out == {
        "@rpath/libC.dylib": "/Users/Shared/spack/pkgC/lib/libC.dylib",
        "@loader_path/../../pkgA/lib": "/Users/Shared/spack/pkgA/lib",
        "@loader_path/../../pkgB/lib": "/Users/Shared/spack/pkgB/lib",
        "/usr/local/lib": "/usr/local/lib",
        "@loader_path/../../pkgA/libA.dylib": "/Users/Shared/spack/pkgA/libA.dylib",
        "@loader_path/../../pkgB/libB.dylib": "/Users/Shared/spack/pkgB/libB.dylib",
        "/usr/local/lib/libloco.dylib": "/usr/local/lib/libloco.dylib",
    }

    out = macho_make_paths_relative(
        "/Users/Shared/spack/pkgC/bin/exeC",
        "/Users/Shared/spack",
        ("/Users/Shared/spack/pkgA/lib", "/Users/Shared/spack/pkgB/lib", "/usr/local/lib"),
        (
            "/Users/Shared/spack/pkgA/libA.dylib",
            "/Users/Shared/spack/pkgB/libB.dylib",
            "/usr/local/lib/libloco.dylib",
        ),
        None,
    )

    assert out == {
        "/Users/Shared/spack/pkgA/lib": "@loader_path/../../pkgA/lib",
        "/Users/Shared/spack/pkgB/lib": "@loader_path/../../pkgB/lib",
        "/usr/local/lib": "/usr/local/lib",
        "/Users/Shared/spack/pkgA/libA.dylib": "@loader_path/../../pkgA/libA.dylib",
        "/Users/Shared/spack/pkgB/libB.dylib": "@loader_path/../../pkgB/libB.dylib",
        "/usr/local/lib/libloco.dylib": "/usr/local/lib/libloco.dylib",
    }

    out = macho_make_paths_normal(
        "/Users/Shared/spack/pkgC/bin/exeC",
        ("@loader_path/../../pkgA/lib", "@loader_path/../../pkgB/lib", "/usr/local/lib"),
        (
            "@loader_path/../../pkgA/libA.dylib",
            "@loader_path/../../pkgB/libB.dylib",
            "/usr/local/lib/libloco.dylib",
        ),
        None,
    )

    assert out == {
        "@loader_path/../../pkgA/lib": "/Users/Shared/spack/pkgA/lib",
        "@loader_path/../../pkgB/lib": "/Users/Shared/spack/pkgB/lib",
        "/usr/local/lib": "/usr/local/lib",
        "@loader_path/../../pkgA/libA.dylib": "/Users/Shared/spack/pkgA/libA.dylib",
        "@loader_path/../../pkgB/libB.dylib": "/Users/Shared/spack/pkgB/libB.dylib",
        "/usr/local/lib/libloco.dylib": "/usr/local/lib/libloco.dylib",
    }


@pytest.fixture()
def mock_download(monkeypatch):
    """Mock a failing download strategy."""

    class FailedDownloadStrategy(spack.fetch_strategy.FetchStrategy):
        def mirror_id(self):
            return None

        def fetch(self):
            raise spack.fetch_strategy.FailedDownloadError(
                urllib.error.URLError("This FetchStrategy always fails")
            )

    @property
    def fake_fn(self):
        return FailedDownloadStrategy()

    monkeypatch.setattr(spack.package_base.PackageBase, "fetcher", fake_fn)


@pytest.mark.parametrize(
    "manual,instr", [(False, False), (False, True), (True, False), (True, True)]
)
@pytest.mark.disable_clean_stage_check
def test_manual_download(mock_download, default_mock_concretization, monkeypatch, manual, instr):
    """
    Ensure expected fetcher fail message based on manual download and instr.
    """

    @property
    def _instr(pkg):
        return f"Download instructions for {pkg.spec.name}"

    spec = default_mock_concretization("pkg-a")
    spec.package.manual_download = manual
    if instr:
        monkeypatch.setattr(spack.package_base.PackageBase, "download_instr", _instr)

    expected = spec.package.download_instr if manual else "All fetchers failed"
    with pytest.raises(spack.error.FetchError, match=expected):
        spec.package.do_fetch()


@pytest.fixture()
def fetching_not_allowed(monkeypatch):
    class FetchingNotAllowed(spack.fetch_strategy.FetchStrategy):
        def mirror_id(self):
            return None

        def fetch(self):
            raise Exception("Sources are fetched but shouldn't have been")

    monkeypatch.setattr(spack.package_base.PackageBase, "fetcher", FetchingNotAllowed())


def test_fetch_without_code_is_noop(default_mock_concretization, fetching_not_allowed):
    """do_fetch for packages without code should be a no-op"""
    pkg = default_mock_concretization("pkg-a").package
    pkg.has_code = False
    pkg.do_fetch()


def test_fetch_external_package_is_noop(default_mock_concretization, fetching_not_allowed):
    """do_fetch for packages without code should be a no-op"""
    spec = default_mock_concretization("pkg-a")
    spec.external_path = "/some/where"
    assert spec.external
    spec.package.do_fetch()


@pytest.mark.parametrize(
    "relocation_dict",
    [
        {"/foo/bar/baz": "/a/b/c", "/foo/bar": "/a/b"},
        # Ensure correctness does not depend on the ordering of the dict
        {"/foo/bar": "/a/b", "/foo/bar/baz": "/a/b/c"},
    ],
)
def test_macho_relocation_with_changing_projection(relocation_dict):
    """Tests that prefix relocation is computed correctly when the prefixes to be relocated
    contain a directory and its subdirectories.

    This happens when relocating to a new place AND changing the store projection. In that case we
    might have a relocation dict like:

    /foo/bar/baz/ -> /a/b/c
    /foo/bar -> /a/b

    What we need to check is that we don't end up in situations where we relocate to a mixture of
    the two schemes, like /a/b/baz.
    """
    original_rpath = "/foo/bar/baz/abcdef"
    result = macho_find_paths(
        [original_rpath],
        deps=[],
        idpath=None,
        old_layout_root="/foo",
        prefix_to_prefix=relocation_dict,
    )
    assert result[original_rpath] == "/a/b/c/abcdef"
