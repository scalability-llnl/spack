# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the `spack verify` command"""
import os

import llnl.util.filesystem as fs

import spack.spec
import spack.store
import spack.util.spack_json as sjson
import spack.verify
from spack.main import SpackCommand

verify = SpackCommand("verify")
install = SpackCommand("install")


def test_single_file_verify_cmd(tmpdir):
    # Test the verify command interface to verifying a single file.
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

    results = verify("-f", filepath, fail_on_error=False)
    print(results)
    assert not results

    os.utime(filepath, (0, 0))
    with open(filepath, "w") as f:
        f.write("I changed.")

    results = verify("-f", filepath, fail_on_error=False)

    expected = ["hash"]
    mtime = os.stat(filepath).st_mtime
    if mtime != data["time"]:
        expected.append("mtime")

    assert results
    assert filepath in results
    assert all(x in results for x in expected)

    results = verify("-fj", filepath, fail_on_error=False)
    res = sjson.load(results)
    assert len(res) == 1
    errors = res.pop(filepath)
    assert sorted(errors) == sorted(expected)


def test_single_spec_verify_cmd(tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery):
    # Test the verify command interface to verify a single spec
    install("libelf")
    s = spack.spec.Spec("libelf").concretized()
    prefix = s.prefix
    hash = s.dag_hash()

    results = verify("/%s" % hash, fail_on_error=False)
    assert not results

    new_file = os.path.join(prefix, "new_file_for_verify_test")
    with open(new_file, "w") as f:
        f.write("New file")

    results = verify("/%s" % hash, fail_on_error=False)
    assert new_file in results
    assert "added" in results

    results = verify("-j", "/%s" % hash, fail_on_error=False)
    res = sjson.load(results)
    assert len(res) == 1
    assert res[new_file] == ["added"]
