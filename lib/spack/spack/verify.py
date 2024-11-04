# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import base64
import hashlib
import os
import stat
from typing import Any, Dict

import llnl.util.tty as tty
from llnl.util.symlink import readlink

import spack.store
import spack.util.file_permissions as fp
import spack.util.spack_json as sjson
from spack.package_base import spack_times_log


def compute_hash(path: str, block_size: int = 1048576) -> str:
    # why is this not using spack.util.crypto.checksum...
    hasher = hashlib.sha1()
    with open(path, "rb") as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            hasher.update(data)
    return base64.b32encode(hasher.digest()).decode()


def create_manifest_entry(path: str) -> Dict[str, Any]:
    try:
        s = os.lstat(path)
    except OSError:
        return {}

    data: Dict[str, Any] = {"mode": s.st_mode, "owner": s.st_uid, "group": s.st_gid}

    if stat.S_ISLNK(s.st_mode):
        data["dest"] = readlink(path)

    elif stat.S_ISREG(s.st_mode):
        data["hash"] = compute_hash(path)
        data["time"] = s.st_mtime
        data["size"] = s.st_size

    return data


def write_manifest(spec):
    manifest_file = os.path.join(
        spec.prefix,
        spack.store.STORE.layout.metadata_dir,
        spack.store.STORE.layout.manifest_file_name,
    )

    if not os.path.exists(manifest_file):
        tty.debug("Writing manifest file: No manifest from binary")

        manifest = {}
        for root, dirs, files in os.walk(spec.prefix):
            for entry in list(dirs + files):
                path = os.path.join(root, entry)
                manifest[path] = create_manifest_entry(path)
        manifest[spec.prefix] = create_manifest_entry(spec.prefix)

        with open(manifest_file, "w") as f:
            sjson.dump(manifest, f)

        fp.set_permissions_by_spec(manifest_file, spec)


def check_entry(path, data):
    res = VerificationResults()

    if not data:
        res.add_error(path, "added")
        return res

    s = os.lstat(path)

    # Check for all entries
    if s.st_uid != data["owner"]:
        res.add_error(path, "owner")
    if s.st_gid != data["group"]:
        res.add_error(path, "group")

    # In the past, `stat(...).st_mode` was stored
    # instead of `lstat(...).st_mode`. So, ignore mode errors for symlinks.
    if not stat.S_ISLNK(s.st_mode) and s.st_mode != data["mode"]:
        res.add_error(path, "mode")
    elif stat.S_ISLNK(s.st_mode) and readlink(path) != data.get("dest"):
        res.add_error(path, "link")
    elif stat.S_ISREG(s.st_mode):
        # Check file contents against hash and listed as file
        # Check mtime and size as well
        if s.st_size != data["size"]:
            res.add_error(path, "size")
        if s.st_mtime != data["time"]:
            res.add_error(path, "mtime")
        if compute_hash(path) != data.get("hash"):
            res.add_error(path, "hash")

    return res


def check_file_manifest(filename):
    dirname = os.path.dirname(filename)

    results = VerificationResults()
    while spack.store.STORE.layout.metadata_dir not in os.listdir(dirname):
        if dirname == os.path.sep:
            results.add_error(filename, "not owned by any package")
            return results
        dirname = os.path.dirname(dirname)

    manifest_file = os.path.join(
        dirname, spack.store.STORE.layout.metadata_dir, spack.store.STORE.layout.manifest_file_name
    )

    if not os.path.exists(manifest_file):
        results.add_error(filename, "manifest missing")
        return results

    try:
        with open(manifest_file, "r") as f:
            manifest = sjson.load(f)
    except Exception:
        results.add_error(filename, "manifest corrupted")
        return results

    if filename in manifest:
        results += check_entry(filename, manifest[filename])
    else:
        results.add_error(filename, "not owned by any package")
    return results


def check_spec_manifest(spec):
    prefix = spec.prefix

    results = VerificationResults()
    manifest_file = os.path.join(
        prefix, spack.store.STORE.layout.metadata_dir, spack.store.STORE.layout.manifest_file_name
    )

    if not os.path.exists(manifest_file):
        results.add_error(prefix, "manifest missing")
        return results

    try:
        with open(manifest_file, "r") as f:
            manifest = sjson.load(f)
    except Exception:
        results.add_error(prefix, "manifest corrupted")
        return results

    for root, dirs, files in os.walk(prefix):
        for entry in list(dirs + files):
            path = os.path.join(root, entry)

            # Do not check manifest file. Can't store your own hash
            if path == manifest_file:
                continue

            # Do not check the install times log file.
            if entry == spack_times_log:
                continue

            data = manifest.pop(path, {})
            results += check_entry(path, data)

    results += check_entry(prefix, manifest.pop(prefix, {}))

    for path in manifest:
        results.add_error(path, "deleted")

    return results


class VerificationResults:
    def __init__(self):
        self.errors = {}

    def add_error(self, path, field):
        self.errors[path] = self.errors.get(path, []) + [field]

    def __add__(self, vr):
        for path, fields in vr.errors.items():
            self.errors[path] = self.errors.get(path, []) + fields
        return self

    def has_errors(self):
        return bool(self.errors)

    def json_string(self):
        return sjson.dump(self.errors)

    def __str__(self):
        res = ""
        for path, fields in self.errors.items():
            res += "%s verification failed with error(s):\n" % path
            for error in fields:
                res += "    %s\n" % error

        if not res:
            res += "No Errors"
        return res
