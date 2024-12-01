# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the `spack.verify` module"""
import os
import shutil
import stat

import pytest

import llnl.util.filesystem as fs
from llnl.util.symlink import symlink

import spack.spec
import spack.store
import spack.util.spack_json as sjson
import spack.verify

pytestmark = pytest.mark.not_on_windows("Tests fail on Win")


def test_link_manifest_entry(tmpdir):
    # Test that symlinks are properly checked against the manifest.
    # Test that the appropriate errors are generated when the check fails.
    file = str(tmpdir.join("file"))
    open(file, "a").close()
    link = str(tmpdir.join("link"))
    os.symlink(file, link)

    data = spack.verify.create_manifest_entry(link)
    assert data["dest"] == file
    assert all(x in data for x in ("mode", "owner", "group"))

    results = spack.verify.check_entry(link, data)
    assert not results.has_errors()

    file2 = str(tmpdir.join("file2"))
    open(file2, "a").close()
    os.remove(link)
    os.symlink(file2, link)

    results = spack.verify.check_entry(link, data)
    assert results.has_errors()
    assert link in results.errors
    assert results.errors[link] == ["link"]


def test_dir_manifest_entry(tmpdir):
    # Test that directories are properly checked against the manifest.
    # Test that the appropriate errors are generated when the check fails.
    dirent = str(tmpdir.join("dir"))
    fs.mkdirp(dirent)

    data = spack.verify.create_manifest_entry(dirent)
    assert stat.S_ISDIR(data["mode"])
    assert all(x in data for x in ("mode", "owner", "group"))

    results = spack.verify.check_entry(dirent, data)
    assert not results.has_errors()

    data["mode"] = "garbage"

    results = spack.verify.check_entry(dirent, data)
    assert results.has_errors()
    assert dirent in results.errors
    assert results.errors[dirent] == ["mode"]


def test_file_manifest_entry(tmpdir):
    # Test that files are properly checked against the manifest.
    # Test that the appropriate errors are generated when the check fails.
    orig_str = "This is a file"
    new_str = "The file has changed"

    file = str(tmpdir.join("dir"))
    with open(file, "w") as f:
        f.write(orig_str)

    data = spack.verify.create_manifest_entry(file)
    assert stat.S_ISREG(data["mode"])
    assert data["size"] == len(orig_str)
    assert all(x in data for x in ("owner", "group"))

    results = spack.verify.check_entry(file, data)
    assert not results.has_errors()

    data["mode"] = 0x99999

    results = spack.verify.check_entry(file, data)
    assert results.has_errors()
    assert file in results.errors
    assert results.errors[file] == ["mode"]

    with open(file, "w") as f:
        f.write(new_str)

    data["mode"] = os.stat(file).st_mode

    results = spack.verify.check_entry(file, data)

    expected = ["size", "hash"]
    mtime = os.stat(file).st_mtime
    if mtime != data["time"]:
        expected.append("mtime")

    assert results.has_errors()
    assert file in results.errors
    assert sorted(results.errors[file]) == sorted(expected)


def test_check_chmod_manifest_entry(tmpdir):
    # Check that the verification properly identifies errors for files whose
    # permissions have been modified.
    file = str(tmpdir.join("dir"))
    with open(file, "w") as f:
        f.write("This is a file")

    data = spack.verify.create_manifest_entry(file)

    os.chmod(file, data["mode"] - 1)

    results = spack.verify.check_entry(file, data)
    assert results.has_errors()
    assert file in results.errors
    assert results.errors[file] == ["mode"]


def test_check_prefix_manifest(tmpdir):
    # Test the verification of an entire prefix and its contents
    prefix_path = tmpdir.join("prefix")
    prefix = str(prefix_path)

    spec = spack.spec.Spec("libelf")
    spec._mark_concrete()
    spec.prefix = prefix

    results = spack.verify.check_spec_manifest(spec)
    assert results.has_errors()
    assert prefix in results.errors
    assert results.errors[prefix] == ["manifest missing"]

    metadata_dir = str(prefix_path.join(".spack"))
    bin_dir = str(prefix_path.join("bin"))
    other_dir = str(prefix_path.join("other"))

    for d in (metadata_dir, bin_dir, other_dir):
        fs.mkdirp(d)

    file = os.path.join(other_dir, "file")
    with open(file, "w") as f:
        f.write("I'm a little file short and stout")

    link = os.path.join(bin_dir, "run")
    symlink(file, link)

    spack.verify.write_manifest(spec)
    results = spack.verify.check_spec_manifest(spec)
    assert not results.has_errors()

    os.remove(link)
    malware = os.path.join(metadata_dir, "hiddenmalware")
    with open(malware, "w") as f:
        f.write("Foul evil deeds")

    results = spack.verify.check_spec_manifest(spec)
    assert results.has_errors()
    assert all(x in results.errors for x in (malware, link))
    assert len(results.errors) == 2

    assert results.errors[link] == ["deleted"]
    assert results.errors[malware] == ["added"]

    manifest_file = os.path.join(
        spec.prefix,
        spack.store.STORE.layout.metadata_dir,
        spack.store.STORE.layout.manifest_file_name,
    )
    with open(manifest_file, "w") as f:
        f.write("{This) string is not proper json")

    results = spack.verify.check_spec_manifest(spec)
    assert results.has_errors()
    assert results.errors[spec.prefix] == ["manifest corrupted"]


def test_single_file_verification(tmpdir):
    # Test the API to verify a single file, including finding the package
    # to which it belongs
    filedir = os.path.join(str(tmpdir), "a", "b", "c", "d")
    filepath = os.path.join(filedir, "file")
    metadir = os.path.join(str(tmpdir), spack.store.STORE.layout.metadata_dir)

    fs.mkdirp(filedir)
    fs.mkdirp(metadir)

    with open(filepath, "w") as f:
        f.write("I'm a file")

    data = spack.verify.create_manifest_entry(filepath)

    manifest_file = os.path.join(metadir, spack.store.STORE.layout.manifest_file_name)

    with open(manifest_file, "w") as f:
        sjson.dump({filepath: data}, f)

    results = spack.verify.check_file_manifest(filepath)
    assert not results.has_errors()

    os.utime(filepath, (0, 0))
    with open(filepath, "w") as f:
        f.write("I changed.")

    results = spack.verify.check_file_manifest(filepath)

    expected = ["hash"]
    mtime = os.stat(filepath).st_mtime
    if mtime != data["time"]:
        expected.append("mtime")

    assert results.has_errors()
    assert filepath in results.errors
    assert sorted(results.errors[filepath]) == sorted(expected)

    shutil.rmtree(metadir)
    results = spack.verify.check_file_manifest(filepath)
    assert results.has_errors()
    assert results.errors[filepath] == ["not owned by any package"]
