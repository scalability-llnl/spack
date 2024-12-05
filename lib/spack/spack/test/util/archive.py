# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import gzip
import hashlib
import os
import shutil
import tarfile
from pathlib import Path, PurePath

import spack.util.crypto
from spack.util.archive import gzip_compressed_tarfile, reproducible_tarfile_from_prefix


def test_gzip_compressed_tarball_is_reproducible(tmpdir):
    """Test gzip_compressed_tarfile and reproducible_tarfile_from_prefix for reproducibility"""

    with tmpdir.as_cwd():
        # Create a few directories
        root = Path("root")
        dir_a = root / "a"
        dir_b = root / "b"
        root.mkdir(mode=0o777)
        dir_a.mkdir(mode=0o777)
        dir_b.mkdir(mode=0o777)

        (root / "y").touch()
        (root / "x").touch()

        (dir_a / "executable").touch(mode=0o777)
        (dir_a / "data").touch(mode=0o666)
        (dir_a / "symlink_file").symlink_to("data")
        (dir_a / "symlink_dir").symlink_to(PurePath("..", "b"))
        try:
            os.link(dir_a / "executable", dir_a / "hardlink")
            hardlink_support = True
        except OSError:
            hardlink_support = False

        (dir_b / "executable").touch(mode=0o777)
        (dir_b / "data").touch(mode=0o666)
        (dir_b / "symlink_file").symlink_to("data")
        (dir_b / "symlink_dir").symlink_to(PurePath("..", "a"))

        # Create the first tarball
        with gzip_compressed_tarfile("fst.tar.gz") as (tar, gzip_checksum_1, tarfile_checksum_1):
            reproducible_tarfile_from_prefix(tar, "root")

        # Expected mode for non-dirs is 644 if not executable, 755 if executable. Better to compute
        # that as we don't know the umask of the user running the test.
        expected_mode = lambda name: (
            0o755 if Path(*name.split("/")).lstat().st_mode & 0o100 else 0o644
        )

        # Verify the tarball contents
        with tarfile.open("fst.tar.gz", "r:gz") as tar:
            # Directories (mode is always 755)
            for dir in ("root", "root/a", "root/b"):
                m = tar.getmember(dir)
                assert m.isdir()
                assert m.mode == 0o755
                assert m.uid == m.gid == 0
                assert m.uname == m.gname == ""

            # Non-executable regular files
            for file in (
                "root/x",
                "root/y",
                "root/a/data",
                "root/b/data",
                "root/a/executable",
                "root/b/executable",
            ):
                m = tar.getmember(file)
                assert m.isreg()
                assert m.mode == expected_mode(file)
                assert m.uid == m.gid == 0
                assert m.uname == m.gname == ""

            # Symlinks
            for file in (
                "root/a/symlink_file",
                "root/a/symlink_dir",
                "root/b/symlink_file",
                "root/b/symlink_dir",
            ):
                m = tar.getmember(file)
                assert m.issym()
                assert m.mode == 0o755
                assert m.uid == m.gid == m.mtime == 0
                assert m.uname == m.gname == ""

            # Verify the symlink targets. Notice that symlink targets are copied verbatim. That
            # means the value is platform specific for relative symlinks within the current prefix,
            # as on Windows they'd be ..\a and ..\b instead of ../a and ../b. So, reproducilility
            # is only guaranteed per-platform currently.
            assert PurePath(tar.getmember("root/a/symlink_file").linkname) == PurePath("data")
            assert PurePath(tar.getmember("root/b/symlink_file").linkname) == PurePath("data")
            assert PurePath(tar.getmember("root/a/symlink_dir").linkname) == PurePath("..", "b")
            assert PurePath(tar.getmember("root/b/symlink_dir").linkname) == PurePath("..", "a")

            # Check hardlink if supported
            if hardlink_support:
                m = tar.getmember("root/a/hardlink")
                assert m.islnk()
                assert m.mode == expected_mode("root/a/hardlink")
                assert m.uid == m.gid == 0
                assert m.uname == m.gname == ""
                # Hardlink targets are always in posix format, as they reference a file that exists
                # in the tarball.
                assert m.linkname == "root/a/executable"

            # Finally verify if entries are ordered by (is_dir, name)
            assert [t.name for t in tar.getmembers()] == [
                "root",
                "root/x",
                "root/y",
                "root/a",
                "root/a/data",
                "root/a/executable",
                *(["root/a/hardlink"] if hardlink_support else []),
                "root/a/symlink_dir",
                "root/a/symlink_file",
                "root/b",
                "root/b/data",
                "root/b/executable",
                "root/b/symlink_dir",
                "root/b/symlink_file",
            ]

        # Delete the current root dir, extract the first tarball, create a second
        shutil.rmtree(root)
        with tarfile.open("fst.tar.gz", "r:gz") as tar:
            tar.extractall()

        # Create the second tarball
        with gzip_compressed_tarfile("snd.tar.gz") as (tar, gzip_checksum_2, tarfile_checksum_2):
            reproducible_tarfile_from_prefix(tar, "root")

        # Verify the .tar.gz checksums are identical and correct
        assert (
            gzip_checksum_1.hexdigest()
            == gzip_checksum_2.hexdigest()
            == spack.util.crypto.checksum(hashlib.sha256, "fst.tar.gz")
            == spack.util.crypto.checksum(hashlib.sha256, "snd.tar.gz")
        )

        # Verify the .tar checksums are identical and correct
        with gzip.open("fst.tar.gz", "rb") as f, gzip.open("snd.tar.gz", "rb") as g:
            assert (
                tarfile_checksum_1.hexdigest()
                == tarfile_checksum_2.hexdigest()
                == spack.util.crypto.checksum_stream(hashlib.sha256, f)
                == spack.util.crypto.checksum_stream(hashlib.sha256, g)
            )
