# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import errno
import hashlib
import io
import os
import pathlib
import tarfile
from contextlib import closing, contextmanager
from gzip import GzipFile
from typing import Callable, Dict, Tuple

from llnl.util.symlink import readlink


class ChecksumWriter(io.BufferedIOBase):
    """Checksum writer computes a checksum while writing to a file."""

    myfileobj = None

    def __init__(self, fileobj, algorithm=hashlib.sha256):
        self.fileobj = fileobj
        self.hasher = algorithm()
        self.length = 0

    def hexdigest(self):
        return self.hasher.hexdigest()

    def write(self, data):
        if isinstance(data, (bytes, bytearray)):
            length = len(data)
        else:
            data = memoryview(data)
            length = data.nbytes

        if length > 0:
            self.fileobj.write(data)
            self.hasher.update(data)

        self.length += length

        return length

    def read(self, size=-1):
        raise OSError(errno.EBADF, "read() on write-only object")

    def read1(self, size=-1):
        raise OSError(errno.EBADF, "read1() on write-only object")

    def peek(self, n):
        raise OSError(errno.EBADF, "peek() on write-only object")

    @property
    def closed(self):
        return self.fileobj is None

    def close(self):
        fileobj = self.fileobj
        if fileobj is None:
            return
        self.fileobj.close()
        self.fileobj = None

    def flush(self):
        self.fileobj.flush()

    def fileno(self):
        return self.fileobj.fileno()

    def rewind(self):
        raise OSError("Can't rewind while computing checksum")

    def readable(self):
        return False

    def writable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.fileobj.tell()

    def seek(self, offset, whence=io.SEEK_SET):
        # In principle forward seek is possible with b"0" padding,
        # but this is not implemented.
        if offset == 0 and whence == io.SEEK_CUR:
            return
        raise OSError("Can't seek while computing checksum")

    def readline(self, size=-1):
        raise OSError(errno.EBADF, "readline() on write-only object")


@contextmanager
def gzip_compressed_tarfile(path):
    """Create a reproducible, gzip compressed tarfile, and keep track of shasums of both the
    compressed and uncompressed tarfile. Reproduciblity is achived by normalizing the gzip header
    (no file name and zero mtime).

    Yields a tuple of the following:
        tarfile.TarFile: tarfile object
        ChecksumWriter: checksum of the gzip compressed tarfile
        ChecksumWriter: checksum of the uncompressed tarfile
    """
    # Create gzip compressed tarball of the install prefix
    # 1) Use explicit empty filename and mtime 0 for gzip header reproducibility.
    #    If the filename="" is dropped, Python will use fileobj.name instead.
    #    This should effectively mimick `gzip --no-name`.
    # 2) On AMD Ryzen 3700X and an SSD disk, we have the following on compression speed:
    # compresslevel=6 gzip default: llvm takes 4mins, roughly 2.1GB
    # compresslevel=9 python default: llvm takes 12mins, roughly 2.1GB
    # So we follow gzip.
    with open(path, "wb") as f, ChecksumWriter(f) as gzip_checksum, closing(
        GzipFile(filename="", mode="wb", compresslevel=6, mtime=0, fileobj=gzip_checksum)
    ) as gzip_file, ChecksumWriter(gzip_file) as tarfile_checksum, tarfile.TarFile(
        name="", mode="w", fileobj=tarfile_checksum
    ) as tar:
        yield tar, gzip_checksum, tarfile_checksum


def default_path_to_name(path: str) -> str:
    """Converts a path to a tarfile name, which uses posix path separators."""
    p = pathlib.PurePath(path)
    # Drop the leading slash on posix and the drive letter on windows, and always format as a
    # posix path.
    return pathlib.PurePath(*p.parts[1:]).as_posix() if p.is_absolute() else p.as_posix()


def reproducible_tarfile_from_prefix(
    tar: tarfile.TarFile,
    prefix: str,
    *,
    include_parent_directories: bool = False,
    skip: Callable[[os.DirEntry], bool] = lambda entry: False,
    path_to_name: Callable[[str], str] = default_path_to_name,
) -> None:
    """Create a tarball from a given directory. Only adds regular files, symlinks and dirs.
    Skips devices, fifos. Preserves hardlinks. Normalizes permissions like git. Tar entries are
    added in depth-first pre-order, with dir entries partitioned by file | dir, and sorted
    lexicographically, for reproducibility. Partitioning ensures only one dir is in memory at a
    time, and sorting improves compression.

    Args:
        tar: tarfile object opened in write mode
        prefix: path to directory to tar (either absolute or relative)
        include_parent_directories: whether to include every directory leading up to ``prefix`` in
            the tarball
        skip: function that receives a DirEntry and returns True if the entry should be skipped,
            whether it is a file or directory. Default implementation does not skip anything.
        path_to_name: function that converts a path string to a tarfile entry name, which should be
            in posix format. Not only is it necessary to transform paths in certain cases, such as
            windows path to posix format, but it can also be used to prepend a directory to each
            entry even if it does not exist on the filesystem. The default implementation drops the
            leading slash on posix and the drive letter on windows for absolute paths, and formats
            as a posix."""

    hardlink_to_tarinfo_name: Dict[Tuple[int, int], str] = dict()

    if include_parent_directories:
        parent_dirs = reversed(pathlib.Path(prefix).parents)
        next(parent_dirs)  # skip the root: slices are supported from python 3.10
        for parent_dir in parent_dirs:
            dir_info = tarfile.TarInfo(path_to_name(str(parent_dir)))
            dir_info.type = tarfile.DIRTYPE
            dir_info.mode = 0o755
            tar.addfile(dir_info)

    dir_stack = [prefix]
    while dir_stack:
        dir = dir_stack.pop()

        # Add the dir before its contents
        dir_info = tarfile.TarInfo(path_to_name(dir))
        dir_info.type = tarfile.DIRTYPE
        dir_info.mode = 0o755
        tar.addfile(dir_info)

        # Sort by name: reproducible & improves compression
        with os.scandir(dir) as it:
            entries = sorted(it, key=lambda entry: entry.name)

        new_dirs = []
        for entry in entries:
            if skip(entry):
                continue

            if entry.is_dir(follow_symlinks=False):
                new_dirs.append(entry.path)
                continue

            file_info = tarfile.TarInfo(path_to_name(entry.path))

            if entry.is_symlink():
                file_info.type = tarfile.SYMTYPE
                file_info.linkname = readlink(entry.path)
                # According to POSIX: "the value of the file mode bits returned in the
                # st_mode field of the stat structure is unspecified." So we set it to
                # something sensible without lstat'ing the link.
                file_info.mode = 0o755
                tar.addfile(file_info)

            elif entry.is_file(follow_symlinks=False):
                # entry.stat has zero (st_ino, st_dev, st_nlink) on Windows: use lstat.
                s = os.lstat(entry.path)

                # Normalize permissions like git
                file_info.mode = 0o755 if s.st_mode & 0o100 else 0o644

                # Deduplicate hardlinks
                if s.st_nlink > 1:
                    ident = (s.st_dev, s.st_ino)
                    if ident in hardlink_to_tarinfo_name:
                        file_info.type = tarfile.LNKTYPE
                        file_info.linkname = hardlink_to_tarinfo_name[ident]
                        tar.addfile(file_info)
                        continue
                    hardlink_to_tarinfo_name[ident] = file_info.name

                # If file not yet seen, copy it
                file_info.type = tarfile.REGTYPE
                file_info.size = s.st_size

                with open(entry.path, "rb") as f:
                    tar.addfile(file_info, f)

        dir_stack.extend(reversed(new_dirs))  # we pop, so reverse to stay alphabetical
